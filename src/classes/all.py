from google.api_core.exceptions import GoogleAPIError
import logging
from logger import trace_id

def decorator_try_except(func):
    """
    A decorator for exception handling in class methods.

    This decorator wraps a class method and captures exceptions of type `GoogleAPIError`.
    If an exception occurs, it is logged as an error using the logging library.
    """
    def try_func(self, *args):
        try:
            return func(self, *args)
        except GoogleAPIError as e:
            logging.error(f"ERROR {e}" , extra={"json_fields": trace_id})
    return try_func

