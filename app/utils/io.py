import pickle
from typing import Any


def save_pickle(obj: Any, path: str) -> None:
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def read_pickle(path: str) -> object:
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj


def recursive_printing_tree(root, spaces=''):
    if root.is_leaf():
        print(spaces, '>', '\\033[32;1m', root.name, '\\033[0m', sep='')
    else:
        print(spaces, '>', root.name, sep='')
        for i, lang in enumerate(root.get_child_languages()):
            recursive_printing_tree(lang, ' |'+spaces)


def tree_to_dict(root):
    return {'name': root.name, 'children': [tree_to_dict(lang) for lang in root.get_child_languages()]}
