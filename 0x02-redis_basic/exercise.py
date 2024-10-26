#!/usr/bin/env python3
""" Module containing the 'Cache' class. """


import redis
import uuid
from functools import wraps
from typing import Any, Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    """ Increases call count every time method is called. """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ Invokes the given method after incrementing its call counter. """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Class containing the 'store' method. """
    def __init__(self) -> None:
        """
            init method for the 'Cache' class. Stores an
            instance of Redis as a private variable and
            flushes the instance using 'flushdb()'.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """Retrieve the stored data, using an optional callable `fn` for conversion."""
        value = self._redis.get(key)

        if not value:
            return None
        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """Retrieve data as a string."""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieve data as an integer."""
        return self.get(key, fn=int)
