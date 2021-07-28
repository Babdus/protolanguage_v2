from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('\033[36;1m', f'func:{f.__name__} took: {te - ts:.4f} sec', '\033[0m')
        return result
    return wrap
