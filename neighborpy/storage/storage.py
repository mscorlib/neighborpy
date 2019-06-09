from typing import Dict, List, Iterable
from nptyping import Array
import numpy as np


class Storage:
    """ Interface for storage adapters. """
    def load_db_keys(self)->List[str]:
        raise NotImplementedError

    def save_db_keys(self, keys: List[str])->bool:
        raise NotImplementedError

    def load_matrix(self, key: str)-> Array[np.float]:
        raise NotImplementedError

    def save_matrix(self, key: str, matrix: Array[np.float])->bool:
        raise NotImplementedError

    def load_id_map(self, key: str)->Dict[str, int]:
        raise NotImplementedError

    def save_id_map(self, key: str, id_map: Dict[str, int]):
        raise NotImplementedError

    def load_index_map(self, key: str)->Dict[int, str]:
        raise NotImplementedError

    def save_index_map(self, key: str, id_map: Dict[int, str]):
        raise NotImplementedError

    # def load_free_map(self, key: str)->List[int]:
    #     raise NotImplementedError
    #
    # def save_free_map(self, key: str, free_map: List[int]):
    #     raise NotImplementedError
