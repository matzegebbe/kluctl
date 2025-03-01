from uuid import uuid4


def is_iterable(obj):
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True

def copy_primitive_value(v):
    if isinstance(v, dict):
        return copy_dict(v)
    if isinstance(v, str) or isinstance(v, bytes):
        return v
    if is_iterable(v):
        return [copy_primitive_value(x) for x in v]
    return v

def copy_dict(a):
    ret = {}
    for k, v in a.items():
        ret[k] = copy_primitive_value(v)
    return ret

def merge_dict(a, b, clone=True):
    if clone:
        a = copy_dict(a)
    if a is None:
        a = {}
    if b is None:
        b = {}
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], clone=False)
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a

def set_default_value(d, n, default):
    if n not in d or d[n] is None:
        d[n] = default

_dummy = str(uuid4())

def _split_path(path):
    if "\\." in path:
        path = path.replace("\\.", _dummy)
        s = path.split(".")
        return [x.replace(_dummy, ".") for x in s]
    else:
        return path.split(".")

def get_dict_value(y, path, default=None):
    s = _split_path(path)

    for x in s:
        if y is None:
            return default
        if x not in y:
            return default
        y = y[x]
    return y

def set_dict_value(y, path, value, do_clone=False):
    s = _split_path(path)
    d = {}
    d2 = d
    for x in s[:-1]:
        d2[x] = {}
        d2 = d2[x]
    d2[s[-1]] = value
    return merge_dict(y, d, do_clone)

def is_empty(o):
    if isinstance(o, dict) or isinstance(o, list):
        return len(o) == 0
    return False

def remove_empty(o):
    if isinstance(o, dict):
        for k in list(o.keys()):
            remove_empty(o[k])
            if is_empty(o[k]):
                del(o[k])
    elif isinstance(o, list):
        i = 0
        while i < len(o):
            v = o[i]
            remove_empty(v)
            if is_empty(v):
                o.pop(i)
            else:
                i += 1
