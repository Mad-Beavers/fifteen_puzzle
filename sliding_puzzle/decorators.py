import time


def timer(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        execution_time = time.time() - start_time
        return result, execution_time

    return wrapper
