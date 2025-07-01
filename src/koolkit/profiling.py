import time
from functools import wraps

# @timeit() decorator -- Prints how long an operation takes.
def timeit(operation_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"{operation_name} took {execution_time:.2f} seconds")
            return result, execution_time
        return wrapper
    return decorator

