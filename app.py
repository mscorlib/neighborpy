import numpy as np
from neighborpy import Engine
from neighborpy.webservice import ResponseModel
from flask import Flask, request, jsonify, Blueprint


app = Flask(__name__)
url_root = '/api/engine/'

DIM = 128
engine = Engine(dim=DIM)


@app.errorhandler(Exception)
def error(e):
    err = {
        'code': e.code,
        'name': e.name,
        'description': e.description
    }
    model = ResponseModel(err, errors=1, message=[err['description']])
    return jsonify(model.__dict__)


@app.route('/ping', methods=['GET'])
def ping():
    model = ResponseModel('pong')
    return jsonify(model.__dict__)


@app.route(url_root + 'db/keys', methods=['GET'])
def get_db_keys():
    data = engine.db_keys

    model = ResponseModel(data)
    return jsonify(model.__dict__)


@app.route(url_root + 'db', methods=['POST'])
def create_db():
    params = request.json

    key = params['key']

    data = engine.create_db(key)

    model = ResponseModel(data)
    return jsonify(model.__dict__)


@app.route(url_root + 'db', methods=['DELETE'])
def delete_db():
    params = request.json

    key = params['key']
    data = engine.delete_db(key)

    model = ResponseModel(data)
    return jsonify(model.__dict__)


@app.route(url_root + 'item', methods=['POST'])
def add_item():
    params = request.json

    key = params['id']
    db_key = params['db_key']
    fx = params['feature']

    data = engine.add_item(db_key=db_key, v=np.array(fx), data=key)

    model = ResponseModel(data)
    return jsonify(model.__dict__)


@app.route(url_root + 'item', methods=['DELETE'])
def delete_item():
    params = request.json
    db_key = params['db_key']
    key = params['key']
    data = engine.delete_item(db_key, key)

    model = ResponseModel(data)
    return jsonify(model.__dict__)


@app.route(url_root + 'items', methods=['POST'])
def add_items():
    params = request.json

    dic = {}
    for item in params:
        db_key = item['db_key']
        key = item['key']
        fx = item['feature']
        dic[key] = np.array(fx)

    data = engine.add_items(db_key, dic)

    model = ResponseModel(data)
    return jsonify(model.__dict__)


@app.route(url_root + 'items', methods=['DELETE'])
def delete_items():
    pass


@app.route(url_root + 'query', methods=['POST'])
def query_items():
    params = request.json
    db_key = params['db_key']
    fx = params['feature']
    k = params['take']

    data = engine.query_item(db_key, np.array(fx), k)

    model = ResponseModel(data)
    return jsonify(model.__dict__)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
