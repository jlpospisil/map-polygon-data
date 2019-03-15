import os
import requests
import pickle
import json

level = 'zip3'
url = 'http://localhost:4000/{}/{}'

dir = os.path.dirname(__file__)
file = os.path.join(dir, 'data', 'state-polygons')
out_dir = os.path.join(dir, 'data', level)

state_ids_file = os.path.join(dir, 'state_ids')
state_ids = pickle.load(open(state_ids_file, 'rb'))

for state_id in state_ids:
    request = requests.get(url.format(level, state_id))

    if request.status_code == 200:
        data = json.loads(request.text)
        file = os.path.join(out_dir, state_id)
        pickle.dump(data, open(file, 'wb'))

    else:
        print('Not found: {}'.format(state_id))
