from importlib import import_module


def load(string):
    parts = string.split('.')
    cls = parts.pop()
    module = import_module('.'.join(parts))
    return getattr(module, cls)
