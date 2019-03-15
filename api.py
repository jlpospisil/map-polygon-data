import os
import pickle
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/<data1>/')
@app.route('/<data1>/<data2>')
@app.route('/<data1>/<data2>/<data3>')
def get_api_dta(data1, data2=None, data3=None):
    try:
        dir = os.path.dirname(__file__)
        data_dir = os.path.join(dir, 'data')
        file = os.path.join(data_dir, data1)

        if data2:
            file = os.path.join(file, data2)

        if data3:
            file = os.path.join(file, data3)

        data = pickle.load(open(file, 'rb'))

        return jsonify(data)

    except Exception:
        return ''


if __name__ == "__main__":
    app.run(host='0.0.0.0')
