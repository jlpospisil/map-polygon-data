import os
import requests
import pickle
import json

url = 'http://localhost:4000/{}/{}'
levels = ['counties', 'zip3']
dir = os.path.abspath(os.path.dirname(__file__))
states_file = os.path.join(dir, 'state_ids')
states = pickle.load(open(states_file, 'rb'))

for level in levels:
    out_dir = os.path.join(dir, 'data', level)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for state in states:
        state_id = state.get('id')

        request = requests.get(url.format(level, state_id))

        if request.status_code == 200:
            data = json.loads(request.text)
            file = os.path.join(out_dir, state_id)
            pickle.dump(data, open(file, 'wb'))

        else:
            print('Not found: {}'.format(state_id))
