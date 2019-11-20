from functools import wraps
import os
import signal
import sys

class MyError(Exception):
    def __init__(self, message, exit_code):
        self.message = message
        self.exit_code = exit_code


def timeout(seconds):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise MyError(f"Time out operation {func.__name__}", 3)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
                return result
            except MyError as ex:
                print(ex.message)
                sys.exit(ex.exit_code)
            finally:
                signal.alarm(0)

        return wraps(func)(wrapper)

    return decorator