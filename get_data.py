import subprocess
import os

urls = {
    'counties': 'http://faculty.baruch.cuny.edu/geoportal/data/esri/usa/census/counties.zip',
    'zip3': 'http://faculty.baruch.cuny.edu/geoportal/data/esri/usa/census/zip3.zip',
    'zip5': 'http://faculty.baruch.cuny.edu/geoportal/data/esri/usa/census/zip_poly.zip',
}

dir = os.path.abspath(os.path.dirname(__file__))
downloads_dir = os.path.join(dir, 'downloads')
js_dir = os.path.join(dir, 'js')

if not os.path.exists(downloads_dir):
    os.mkdir(downloads_dir)

for level in urls:
    file_name = '{}.zip'.format(level)
    file = os.path.join(downloads_dir, file_name)

    # If the file doesn't exist, download it
    if not os.path.exists(file):
        cmd = 'wget {} -O {}'.format(urls.get(level), file)
        subprocess.call(cmd, shell=True)

    # Unzip the downloaded file
    subprocess.call('cd {} && unzip -o {} -d {}'.format(downloads_dir, file_name, level), shell=True)

    # Convert the shapefile to geoJSON
    data_dir = os.path.join(downloads_dir, level)
    geojson_file = os.path.join(js_dir, '{}.json'.format(level))
    cmd = 'ogr2ogr -f geoJSON {} *.shp'.format(geojson_file)
    subprocess.call('cd {} && {}'.format(data_dir, cmd), shell=True)
