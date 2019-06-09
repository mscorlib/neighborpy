#

import struct
import numpy as np
import redis
from neighborpy.storage.storage import Storage

pool = redis.ConnectionPool(host='192.168.1.126', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)


class RedisStorage(Storage):
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_db(self, db_key):
        key = self._format_db_key(db_key)
        return self.redis.get(key)

    def get_dbs(self):
        key = self._format_db_key('*')
        return self.redis.get(key)
        pass

    def create_db(self, db_key):
        key = self._format_db_key(db_key)
        self.redis.set(key, '')
        pass

    def delete_db(self, db_key):
        r.flushdb()
        key = self._format_db_key(db_key)
        vector_key = self._format_vector_key(db_key)
        id_map_key = self._format_id_map(db_key, '*')
        free_vector_key = self._format_free_vector(db_key)

        self.redis.delete(key)
        self.redis.delete(vector_key)
        self.redis.delete(id_map_key)
        self.redis.delete(free_vector_key)

    def load_vectors(self, db_key):
        key = self._format_vector_key(db_key)
        encoded = self.redis.get(key)
        h, w = struct.unpack('>II', encoded[:8])
        a = np.frombuffer(encoded, dtype=np.uint16, offset=8).reshape(h, w)
        return a

    def save_vectors(self, db_key, vs):
        key = self._format_vector_key(db_key)
        h, w = vs.shape
        shape = struct.pack('>II', h, w)
        encoded = shape + vs.tobytes()
        self.redis.set(key, encoded)

    def _format_db_key(self, db_key):
        return 'Engine::Repository::{}'.format(db_key)

    def _format_vector_key(self, db_key):
        return 'Engine::Vector::{}'.format(db_key)

    def _format_id_map(self, db_key, id):
        return 'Engine::IdMap::{}::{}'.format(db_key, id)

    def _format_free_vector(self, db_key):
        return 'Engine::FreeVector::{}'.format(db_key)