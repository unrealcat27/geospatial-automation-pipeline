import json
import os
import sys

# Dynamically ensure the src directory is accessible to Python
folder_proyek = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if folder_proyek not in sys.path:
    sys.path.append(folder_proyek)

from src.data_loader import load_filter_dan_reproject

def jalankan_pipeline_utama(nama_file_klien: str, nama_config_json: str, engine_choice: str = "qgis"):
    """
    Main pipeline controller.
    Routes tasks to the selected engine without breaking the overall framework.
    """
    # 1. Resolve absolute paths dynamically
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    jalur_file_klien = os.path.join(base_dir, "inputs", nama_file_klien)
    jalur_config_json = os.path.join(base_dir, "config", nama_config_json)
    output_dir = os.path.join(base_dir, "outputs")
    
    print(f"[*] Starting Pipeline using engine: {engine_choice.upper()}")
    print("[1] Routing client data to validation gateway...")
    
    # 2. Universal Data Rescue Gateway
    layer_rapi, status = load_filter_dan_reproject(jalur_file_klien)
    if "ERROR" in status:
        print(f"[X] PIPELINE HALTED: {status}. Check client input file.")
        return False
        
    # 3. Read universal JSON configurations
    with open(jalur_config_json, 'r') as f:
        daftar_analisis = json.load(f)
        
    # 4. Engine Selector Switchboard
    if engine_choice.lower() == "qgis":
        print("[2] Initializing QGIS Desktop Worker Engine...")
        from src.engines.qgis_engine import jalankan_qgis_tasks
        
        # Route tasks to QGIS engine
        semua_hasil = jalankan_qgis_tasks(layer_rapi, daftar_analisis)
        
        # Save results persistently instead of volatile memory layers
        # (We will implement the hard exporter inside the qgis_engine)
        
    elif engine_choice.lower() == "standalone":
        print("[2] Initializing Headless Standalone Engine (GeoPandas/Rasterio)...")
        from src.engines.standalone_engine import jalankan_standalone_tasks
        
        # Route tasks to independent Python engine
        semua_hasil = jalankan_standalone_tasks(layer_rapi, daftar_analisis, output_dir)
        
    else:
        print(f"[X] ERROR: Engine '{engine_choice}' is not recognized.")
        return False

    print("[*] Pipeline Process Finished Successfully!")
    return True

if __name__ == "__main__":
    # Test execution routing locally
    jalankan_pipeline_utama("lahan_klien.geojson", "analisis_config.json", engine_choice="qgis")
