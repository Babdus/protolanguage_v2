import pickle
from typing import Any


def save_pickle(obj: Any, path: str) -> None:
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def read_pickle(path: str) -> object:
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj
