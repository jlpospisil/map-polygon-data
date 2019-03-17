import os
import pickle
import json

levels = ['zip3', 'zip5']
dir = os.path.abspath(os.path.dirname(__file__))
geojson = dict()

for l in levels:
    file = os.path.join(dir, 'data', '{}.json'.format(l))

    with open(file) as f:
        geojson[l] = json.load(f)

    geojson[l] = geojson[l].get('features', [])


def create_polygons_from_geometry(geometry):
    multiple = geometry.get('type', '').lower() == 'multipolygon'
    coordinates = geometry.get('coordinates', [])

    if multiple:
        coordinates = [c[0] for c in coordinates]

    return [[{'lat': p[1], 'lng': p[0]} for p in c] for c in coordinates]


def get_api_data(level, id):
    polygons = geojson[level]

    if level == 'zip5':
        polygons = [{
            'id': p.get('properties', {}).get('ZIP'),
            'polygons': create_polygons_from_geometry(p.get('geometry', {}))
        } for p in polygons if p.get('properties', {}).get('ZIP', '').startswith(id)]

    elif level == 'zip3':
        polygons = [{
            'id': p.get('properties', {}).get('ZIP3'),
            'polygons': create_polygons_from_geometry(p.get('geometry', {}))
        } for p in polygons if p.get('properties', {}).get('STATE', '') == id]

    return polygons


if __name__ == "__main__":
    dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(dir, 'data')
    zip3_dir = os.path.join(data_dir, 'zip3')
    zip5_dir = os.path.join(data_dir, 'zip5')
    states_file = os.path.join(data_dir, 'state-ids')
    states = pickle.load(open(states_file, 'rb'))

    os.mkdir(zip3_dir)
    os.mkdir(zip5_dir)

    for state in states:
        # Process zip3 data
        state_id = state.get('id')
        data = get_api_data('zip3', state_id)
        file = os.path.join(zip3_dir, state_id)
        pickle.dump(data, open(file, 'wb'))

        # TODO: process county data here

        # For each zip3, process each zip5
        for zip3 in [d.get('id') for d in data]:
            data = get_api_data('zip5', zip3)
            file = os.path.join(zip5_dir, zip3)
            pickle.dump(data, open(file, 'wb'))
