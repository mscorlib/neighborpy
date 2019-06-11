import redis
from flask import Flask

from neighborpy.engine import Engine
from neighborpy.storage.storage_redis import RedisStorage
from neighborpy.webservice.apis import construct_blueprint

DIM = 128
app = Flask(__name__)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
r = redis.StrictRedis(connection_pool=pool)

engine = Engine(dim=DIM, storage_provider=RedisStorage(r))

bp = construct_blueprint(engine)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
