import numpy as np

from neighborpy.engine import Engine
from neighborpy.webservice.responsemodel import ResponseModel
from flask import request, jsonify, Blueprint

DIM = 128


def construct_blueprint(engine: Engine= Engine(dim=DIM)):

    engine_api = Blueprint('engine_api', __name__, url_prefix='/api/engine/')

    _engine = engine

    @engine_api.errorhandler(KeyError)
    def key_error(e):
        err = {
            'name': 'KeyError',
            'description': 'key: [{}] not found'.format(str(e))
        }
        model = ResponseModel(errors=1, message=[err['description']])
        return jsonify(model.__dict__)

    @engine_api.errorhandler(Exception)
    def error(e):
        # err = {
        #     # 'code': e.code,
        #     'name': e.name,
        #     'description': e.description
        # }
        model = ResponseModel(errors=1, message=[str(e)])
        return jsonify(model.__dict__)

    @engine_api.route('ping', methods=['GET'])
    def ping():
        model = ResponseModel('pong')
        return jsonify(model.__dict__)

    @engine_api.route('db/exist', methods=['POST'])
    def db_exist():
        params = request.json

        key = params['key']

        data = _engine.is_db_exist(key)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('db/keys', methods=['GET'])
    def get_db_keys():
        data = _engine.db_keys

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('db', methods=['POST'])
    def create_db():
        params = request.json

        key = params['key']

        data = _engine.create_db(key)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('db', methods=['DELETE'])
    def delete_db():
        params = request.json

        key = params['key']
        data = _engine.delete_db(key)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('item', methods=['POST'])
    def add_item():
        params = request.json

        key = params['key']
        db_key = params['db_key']
        fx = params['feature']

        data = _engine.add_item(db_key=db_key, v=np.array(fx), data=key)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('item', methods=['DELETE'])
    def delete_item():
        params = request.json
        db_key = params['db_key']
        key = params['key']
        data = _engine.delete_item(db_key, key)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('items', methods=['POST'])
    def add_items():
        params = request.json

        dic = {}
        for item in params:
            db_key = item['db_key']
            key = item['key']
            fx = item['feature']
            dic[key] = np.array(fx)

        data = _engine.add_items(db_key, dic)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('items', methods=['DELETE'])
    def delete_items():
        params = request.json

        key = params['key']
        db_key = params['db_key']

        data = _engine.delete_item(db_key=db_key, data=key)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    @engine_api.route('query', methods=['POST'])
    def query_items():
        params = request.json
        db_key = params['db_key']
        fx = params['feature']
        k = params['take']

        data = _engine.query_item(db_key, np.array(fx), k)

        model = ResponseModel(data)
        return jsonify(model.__dict__)

    return engine_api
