import os
import pickle
import json

levels = ['counties', 'zip3', 'zip5']
geojson = dict()
dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(dir, 'data')
counties_dir = os.path.join(data_dir, 'counties')
zip3_dir = os.path.join(data_dir, 'zip3')
zip5_dir = os.path.join(data_dir, 'zip5')
states_file = os.path.join(data_dir, 'state-ids')
states = pickle.load(open(states_file, 'rb'))

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


def state_name(state_id):
    state = next(s for s in states if s['id'] == state_id)
    return state.get('name', '') if state else ''


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

    elif level == 'counties':
        polygons = [{
            'id': '{} - {}'.format(p.get('properties', {}).get('STATE_NAME'), p.get('properties', {}).get('NAME')),
            'polygons': create_polygons_from_geometry(p.get('geometry', {}))
        } for p in polygons if p.get('properties', {}).get('STATE_NAME', '').lower() == state_name(id).lower()]

    return polygons


if __name__ == "__main__":
    for state in states:
        # Process county data
        if not os.path.exists(counties_dir):
            os.mkdir(counties_dir)
        data = get_api_data('counties', state_id)
        if len(data) > 0:
            file = os.path.join(counties_dir, state_id)
            pickle.dump(data, open(file, 'wb'))

        # Process zip3 data
        if not os.path.exists(zip3_dir):
            os.mkdir(zip3_dir)
        state_id = state.get('id')
        data = get_api_data('zip3', state_id)
        if len(data) > 0:
            file = os.path.join(zip3_dir, state_id)
            pickle.dump(data, open(file, 'wb'))

        # For each zip3, process each zip5
        for zip3 in [d.get('id') for d in data]:
            if not os.path.exists(zip5_dir):
                os.mkdir(zip5_dir)
            data = get_api_data('zip5', zip3)
            if len(data) > 0:
                file = os.path.join(zip5_dir, zip3)
                pickle.dump(data, open(file, 'wb'))
