import functools
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def catch_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as exception:
            logger.error(repr(exception))
    return func
