from typing import List, Dict, Any, Iterable, Sequence, Tuple, NamedTuple
from nptyping import Array
import numpy as np

from neighborpy.storage.storage import Storage


class MemoryStorage(Storage):
    _db_keys: List[str]
    _matrices: Dict[str, Array[np.float]]
    _id_maps: Dict[str, Dict[str, int]]
    _index_maps: Dict[str, Dict[int, str]]
    # _free_maps: Dict[str, List[int]]

    def __init__(self):
        self._db_keys = []
        self._matrices = {}
        self._id_maps = {}
        self._index_maps = {}
        # self._free_maps = {}

    def load_db_keys(self) -> List[str]:
        return self._db_keys

    def save_db_keys(self, keys: Array[np.float]) -> bool:
        self._db_keys = keys

    def load_matrix(self, key: str) -> Array[np.float]:

        if key in self._matrices:
            return self._matrices[key]
        return None

    def save_matrix(self, key: str, matrix: List[List[float]]) -> bool:
        self._matrices[key] = matrix

    def load_id_map(self, key: str) -> Dict[str, int]:
        if key in self._id_maps:
            return self._id_maps[key]
        return None

    def save_id_map(self, key: str, id_map: Dict[str, int]):
        self._id_maps[key] = id_map

    def load_index_map(self, key: str)->Dict[int, str]:
        if key in self._index_maps:
            return self._index_maps[key]
        return None

    def save_index_map(self, key: str, index_map: Dict[int, str]):
        self._index_maps[key] = index_map

    # def load_free_map(self, key: str) -> List[int]:
    #     if key in self._free_maps:
    #         return self._free_maps[key]
    #     return None
    #
    # def save_free_map(self, key: str, free_map: List[int]):
    #     self._free_maps[key] = free_map
