from google.appengine.api import memcache
import logging
import functools
# if CACHE_TIMEOUT_OVERRIDE is -1: never cache
# if CACHE_TIMEOUT_OVERRIDE is 0: forever cache
CACHE_TIMEOUT_OVERRIDE = 1200


def cached(time=1200):
    """
    Decorator that caches the result of a method for the specified time in seconds.
    Use it as:
    @cached(time=1200)
    def functionToCache(arguments):
      ...

    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            # if CACHE_TIMEOUT_OVERRIDE is -1: never cache
            # if CACHE_TIMEOUT_OVERRIDE is 0: forever cache
            key = '%s%s%s' % (function.__name__, str(args), str(kwargs))
            value = memcache.get(key)
            logging.info('Cache lookup for %s, found? %s', key,
                         CACHE_TIMEOUT_OVERRIDE != -1 and value != None)
            if (CACHE_TIMEOUT_OVERRIDE == -1 ) or  not value:
                value = function(*args, **kwargs)
                memcache.set(key, value, time=time)
            return value
        return wrapper
    return decorator
