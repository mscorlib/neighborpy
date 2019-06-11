#

import struct
from typing import Dict, List
import json
import numpy as np
from nptyping import Array
from redis import Redis
from neighborpy.storage.storage import Storage


def _format_matrix_key(db_key):
    return 'Engine::Matrix::{}'.format(db_key)


def _format_id_map(db_key):
    return 'Engine::IdMap::{}'.format(db_key)


def _format_index_map(db_key):
    return 'Engine::IndexMap::{}'.format(db_key)


class RedisStorage(Storage):
    redis: Redis
    _r_db_key = 'Engine::Db::Keys'

    def __init__(self, redis_client):
        self.redis = redis_client

    def load_db_keys(self) -> List[str]:
        try:
            ks = self.redis.get(self._r_db_key)
            return json.loads(ks)
        except:
            return []

    def save_db_keys(self, keys: List[str]) -> bool:
        val = json.dumps(keys)
        self.redis.set(self._r_db_key, val)
        return True

    def load_matrix(self, key: str) -> Array[np.float]:
        try:
            key = _format_matrix_key(key)
            encoded = self.redis.get(key)
            h, w = struct.unpack('>II', encoded[:8])
            a = np.frombuffer(encoded, dtype=np.float, offset=8).reshape(h, w)
            return a
        except:
            return None

    def save_matrix(self, key: str, matrix: Array[np.float]) -> bool:
        key = _format_matrix_key(key)
        h, w = matrix.shape
        shape = struct.pack('>II', h, w)
        encoded = shape + matrix.tobytes()
        self.redis.set(key, encoded)
        return True

    def load_id_map(self, key: str) -> Dict[str, int]:
        try:
            k = _format_id_map(key)
            map = self.redis.get(k)
            return json.loads(map)
        except:
            return None

    def save_id_map(self, key: str, id_map: Dict[str, int]):
        k = _format_id_map(key)
        val = json.dumps(id_map)
        self.redis.set(k, val)
        return True

    def load_index_map(self, key: str) -> Dict[int, str]:
        try:
            k = _format_index_map(key)
            map = self.redis.get(k)
            return json.loads(map)
        except:
            return None

    def save_index_map(self, key: str, id_map: Dict[int, str]):
        k = _format_index_map(key)
        val = json.dumps(id_map)
        self.redis.set(k, val)
        return True

    # def delete_db(self, db_key):
    #     r.flushdb()
    #     key = self._format_db_key(db_key)
    #     vector_key = self._format_vector_key(db_key)
    #     id_map_key = self._format_id_map(db_key, '*')
    #     free_vector_key = self._format_free_vector(db_key)
    #
    #     self.redis.delete(key)
    #     self.redis.delete(vector_key)
    #     self.redis.delete(id_map_key)
    #     self.redis.delete(free_vector_key)

