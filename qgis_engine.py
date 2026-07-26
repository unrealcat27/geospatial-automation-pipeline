import os
from qgis import processing
from qgis.core import QgsProject, QgsVectorFileWriter
from PyQt5.QtGui import QColor
from qgis.core import QgsSimpleFillSymbolLayer

# [RECYCLED FROM STYLER.PY]
WARNA_PRESET = {
    "MERAH_BAHAYA": (255, 0, 0, 120),
    "HIJAU_AMAN": (0, 255, 0, 80),
    "BIRU_AIR": (0, 120, 255, 100),
    "KUNING_PERINGATAN": (255, 200, 0, 100),
    "ABU_BANGUNAN": (128, 128, 128, 150)
}

def warnai_polygon_dengan_preset(layer, nama_warna: str, lebar_garis: float = 0.6):
    """Recycled styling engine from your original code."""
    r, g, b, alpha = WARNA_PRESET.get(nama_warna, WARNA_PRESET["ABU_BANGUNAN"])
    warna_isi = QColor(r, g, b, alpha)
    warna_garis = QColor(r, g, b, 255)
    
    simbol_layer = QgsSimpleFillSymbolLayer.create({
        'color': f'{warna_isi.red()},{warna_isi.green()},{warna_isi.blue()},{warna_isi.alpha()}',
        'outline_color': f'{warna_garis.red()},{warna_garis.green()},{warna_garis.blue()},{warna_garis.alpha()}',
        'outline_width': str(lebar_garis),
        'style': 'solid',
        'outline_style': 'solid'
    })
    
    if simbol_layer is not None:
        layer.renderer().setSymbol(simbol_layer)
        layer.triggerRepaint()
        print(f"[+] Layer styled inside QGIS using preset: {nama_warna}")

# [UPGRADED FLEXIBLE WORKER]
def jalankan_qgis_tasks(layer_meter, daftar_analisis: list):
    """
    Translates flexible task configurations into QGIS Native processing commands
    and saves hard copies permanently to the outputs folder.
    """
    # Find the base output path dynamically
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_output = os.path.join(base_dir, "outputs")
    
    hasil_semua_analisis = []
    
    for item in daftar_analisis:
        action = item['action']
        nama_analisis = item['nama_analisis']
        warna = item.get('warna_preset', 'ABU_BANGUNAN')
        
        print(f"[ ] Running QGIS Processing for: {nama_analisis} ({action})")
        
        # 1. Map flexible plain-English commands to QGIS specific tools
        if action == "buffer":
            qgis_algo = "native:buffer"
            # Translate client-friendly variables to what QGIS expects
            params = {
                'INPUT': layer_meter,
                'DISTANCE': item['parameter'].get('distance_meters', 10.0),
                'DISSOLVE': item['parameter'].get('dissolve', True),
                'OUTPUT': 'memory:temp_buffer'
            }
        elif action == "slope":
            # Note: Slope needs a Raster layer. We flag it here so it gracefully informs you.
            print(f"[!] Warning: Action '{action}' requires a terrain raster input.")
            continue
        else:
            print(f"[-] Action '{action}' not recognized by QGIS engine.")
            continue
            
        try:
            # 2. Execute via desktop engine
            output_layer = processing.run(qgis_algo, params)['OUTPUT']
            
            # 3. FIX THE VOLATILE MEMORY PROBLEM: Save hard copy permanently to /outputs
            nama_file_bersih = nama_analisis.lower().replace(" ", "_") + ".geojson"
            jalur_simpan_permanen = os.path.join(folder_output, nama_file_bersih)
            
            # Write out to physical storage as a GeoJSON file
            QgsVectorFileWriter.writeAsVectorFormatV3(
                output_layer, 
                jalur_simpan_permanen, 
                QgsProject.instance().transformContext(), 
                QgsVectorFileWriter.SaveVectorOptions()
            )
            print(f"[+] Saved hard copy permanently to: outputs/{nama_file_bersih}")
            
            # 4. Apply visual styling to the temporary layout for QGIS interface screen
            warnai_polygon_dengan_preset(output_layer, warna)
            QgsProject.instance().addMapLayer(output_layer)
            
            hasil_semua_analisis.append(output_layer)
            
        except Exception as e:
            print(f"[-] Failed executing QGIS task {nama_analisis}: {str(e)}")
            
    return hasil_semua_analisis
