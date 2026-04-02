import time
from functools import wraps


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Starting {func.__name__}...")
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Finished {func.__name__} in {duration:.2f} seconds.")
        return result

    return wrapper
