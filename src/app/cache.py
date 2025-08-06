cache_store = {"fib": {}, "pow": {}, "factorial": {}}


def init_cache():
    global cache_store
    cache_store = {"fib": {}, "pow": {}, "factorial": {}}


def check_cache(operation: str, key: int):
    return cache_store.get(operation, {}).get(key)


def set_cache(operation: str, key: int, value):
    if operation not in cache_store:
        cache_store[operation] = {}
    cache_store[operation][key] = value
