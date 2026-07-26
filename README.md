# Flexible Geospatial Automation Pipeline

An enterprise-ready Python framework designed to automate geospatial data cleaning, 
coordinate reprojection, and batch spatial analysis. 

## Key Features
* **Dynamic Coordinate Correction:** Automatically detects raw coordinate systems and reprojects spatial data into local, metric-accurate UTM zones using custom geometric calculations.
* **Engine Agnostic Architecture:** Built to switch dynamically between desktop processing (via PyQGIS) and headless cloud execution (via standalone Python spatial libraries).
* **Data Rescue Gateway:** Built-in validation layers to automatically catch, log, and handle corrupt, empty, or misaligned vector and raster datasets before processing begins.
