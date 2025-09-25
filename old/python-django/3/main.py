import time
import threading
from collections import OrderedDict


def conditional_cache(expiry, condition, max_size=5):
    def decorator(func):
        cache = OrderedDict()
        lock = threading.Lock()
        def wrapper(*args, **kwargs):
            if not condition(*args, **kwargs):
                return None
            
            # our x satisfied the condition
            key = (args, tuple(sorted(kwargs.items())))
            
            with lock:
                if key in cache:
                    value, exp = cache[key]
                    if time.time() < exp:
                        cache.move_to_end(key)
                        return value
                    else:
                        del cache[key]
                
                result = func(*args, **kwargs)
                # save in cache
                cache[key] = (result, time.time() + expiry)
                
                if len(cache) > max_size:
                    cache.popitem(last=False)
            return result
        return wrapper
    return decorator

# def is_positive(x):
#     return x > 0

# @conditional_cache(expiry=5, condition=is_positive)
# def compute_square(x):
#     print(f"Computing square of {x}")
#     return x * x

# print(compute_square(3))
# time.sleep(2)
# print(compute_square(3))
# time.sleep(4)
# print(compute_square(3))
# print(compute_square(-3))
