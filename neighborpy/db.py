from typing import List, Dict
import numpy as np
import pandas as pd
from nptyping import Array
from sklearn.neighbors import BallTree


class Db:
    _key: str
    _dim: int
    tree: BallTree
    matrix: Array[np.float]
    id_map: Dict[str, int]
    index_map: Dict[str, str]
    # free_map: List[int]

    def __init__(self, key: str, dim: int):
        self._key = key
        self._dim = dim
        matrix = np.zeros([1, self._dim])
        matrix[0] = np.random.randn(self._dim)
        self.matrix = matrix
        self.id_map = {}
        self.index_map = {}
        # self.free_map = []

    @property
    def key(self):
        return self._key

    @property
    def dim(self):
        return self._dim

    def count(self):
        return len(self.matrix)
