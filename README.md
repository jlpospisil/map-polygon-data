Getting Started
------------------------------------------
1. Install dependencies:
    ```
    brew install wget gdal
    ```
    
2. Create and prepare a new python virtualenv
    ```
    python3 -m venv venv
    source venv/bin/activate    
    pip install -r requirements.txt
    ```
    
3. Run the following command to download the shapefiles and convert them to geoJSON:
    ```
    python get_data.py
    ```


Shapefile Information
------------------------------------------

Downloads:
    https://www.baruch.cuny.edu/confluence/display/geoportal/ESRI+USA+Data

Manually convert shapefile to geoJSON:

    ogr2ogr -f geoJSON output.json input.shp
