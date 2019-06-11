import time
from typing import List, Dict
import numpy as np
from nptyping import Array
from sklearn.neighbors import BallTree
from sklearn.metrics.pairwise import cosine_similarity
from neighborpy.exception import EngineException
from neighborpy.storage.storage import Storage
from neighborpy.storage.storage_memory import MemoryStorage
from neighborpy.db import Db


class Engine:
    _dim: int
    _leaf_size: int
    _dbs: Dict[str, Db]
    _db_keys: List[str]
    _storage: Storage

    def __init__(self,
                 dim: int = 128,
                 leaf_size: int = 500,
                 storage_provider: Storage = MemoryStorage()):

        self._dim = dim
        self._leaf_size = leaf_size
        self._dbs = {}
        self._storage = storage_provider
        self._load_db_keys()

    def is_db_exist(self, key: str) -> bool:
        return key in self._db_keys

    @property
    def db_keys(self):
        return self._db_keys

    def create_db(self, key: str) -> bool:
        if key in self._db_keys:
            raise EngineException('db exist', 'db key: [{}] is exist!'.format(key))

        self._db_keys.append(key)
        self._storage.save_db_keys(self._db_keys)
        return True

    def _load_db(self, key: str) -> bool:
        if key not in self._db_keys:
            raise EngineException('db not found', 'db key: [{}] not found!'.format(key))

        if key in self._dbs:
            return True

        db = Db(key, dim=self._dim)

        db.matrix = self._storage.load_matrix(key)
        if db.matrix is None:
            db.matrix = np.zeros([1, self._dim])

        db.id_map = self._storage.load_id_map(key)
        if db.id_map is None:
            db.id_map = {}

        db.index_map = self._storage.load_index_map(key)
        if db.index_map is None:
            db.index_map = {}

        # db.free_map = self._storage.load_free_map(key)
        # if db.free_map is None:
        #     db.free_map = []

        db.tree = BallTree(db.matrix, leaf_size=self._leaf_size)

        self._dbs[key] = db

        return True

    def save_db(self, db: Db):
        self._storage.save_matrix(db.key, db.matrix)
        self._storage.save_id_map(db.key, db.id_map)
        self._storage.save_index_map(db.key, db.index_map)
        # self._storage.save_free_map(db.key, db.free_map)

    def delete_db(self, key: str):
        raise NotImplementedError

    def _load_db_keys(self):
        keys = self._storage.load_db_keys()
        if keys is None:
            keys = []
        self._db_keys = keys

    def add_item(self, db_key: str, v: Array[np.float], data: str) -> bool:
        if db_key not in self._db_keys:
            raise EngineException('db not found', 'db key: [{}] not found!'.format(db_key))

        if db_key not in self._dbs:
            self._load_db(db_key)

        db = self._dbs[db_key]

        # if len(db.free_map) > 0:
        #     index = db.free_map.pop()
        #     db.matrix[index, :] = v
        #
        # else:
        #     index = np.size(db.matrix, 0)
        #     db.matrix = np.append(db.matrix, [v], axis=0)

        index = np.size(db.matrix, 0)
        db.matrix = np.append(db.matrix, [v], axis=0)

        db.id_map[data] = index
        db.index_map[str(index)] = data
        tree = BallTree(db.matrix, leaf_size=self._leaf_size)
        db.tree = tree

        self.save_db(db)

        return True

    def add_items(self, db_key: str, vs: Dict[str, Array[np.float]]):
        if db_key not in self._db_keys:
            raise EngineException('db not found', 'db key: [{}] not found!'.format(db_key))

        if db_key not in self._dbs:
            self._load_db(db_key)

        db = self._dbs[db_key]

        c1 = time.clock()

        count = 0
        start = np.size(db.matrix, 0)
        values = list(vs.values())
        db.matrix = np.append(db.matrix, values, axis=0)
        for k in vs:
            index = start + count
            count += 1
            db.id_map[k] = index
            db.index_map[str(index)] = k
        # for k in vs:
        #     if len(db.free_map) > 0:
        #         index = db.free_map.pop()
        #         db.matrix[index, :] = vs[k]
        #     else:
        #         index = np.size(db.matrix, 0)
        #         db.matrix = np.append(db.matrix, [vs[k]], axis=0)
        #     db.id_map[k] = index
        #     db.index_map[index] = k

        c2 = time.clock()
        print('build matrix %d, clock: %0.6f' % (len(vs), (c2 - c1)))

        # d_count = db.count()
        # c1 = time.clock()
        tree = BallTree(db.matrix, leaf_size=self._leaf_size)
        # c2 = time.clock()
        # print('build tree clock: %0.6f' %(c2 - c1))
        db.tree = tree

        self.save_db(db)

    def delete_item(self, db_key: str, data: str) -> bool:
        if db_key not in self._db_keys:
            raise EngineException('db not found', 'db key: [{}] not found!'.format(db_key))

        if db_key not in self._dbs:
            self._load_db(db_key)

        db = self._dbs[db_key]

        index = db.id_map[data]
        # rows, cols = db.matrix.shape
        db.matrix = np.delete(db.matrix, index, axis=0)
        del db.id_map[data]

        db.index_map = {}
        count = 1
        for key in db.id_map:
            db.id_map[key] = count
            db.index_map[str(count)] = key
            count += 1

        # db.matrix[index] = np.random.randn(self._dim)
        #
        # del db.id_map[data]
        #
        # db.free_map.append(index)

        tree = BallTree(db.matrix, leaf_size=self._leaf_size)
        db.tree = tree

        self.save_db(db)

        return True

    def query_item(self, db_key, v: Array[np.float], take=1)->Dict[str, float]:
        if db_key not in self._db_keys:
            raise EngineException('db not found', 'db key: [{}] not found!'.format(db_key))

        if db_key not in self._dbs:
            self._load_db(db_key)

        db = self._dbs[db_key]

        # query
        dist, ind = db.tree.query([v], k=take+1)

        idx = ind[0].tolist()

        if 0 in idx:
            idx.remove(0)

        # build result matrix
        index = 0
        count = len(idx)
        matrix = np.zeros((count, db.dim))
        for k in idx:
            matrix[index] = db.matrix[k]
            index += 1

        # build query matrix
        qm = np.zeros((1, db.dim))
        qm[0] = v

        # get cosine similarity
        distances = cosine_similarity(qm, matrix)

        keys = [db.index_map[str(index)] for index in idx]
        result = dict(zip(keys, distances[0].tolist()))

        # remove last
        if len(result) > take:
            for k in list(result)[-1:]:
                del result[k]

        return result
