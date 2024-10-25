#!/usr/bin/env python3
""" Module containing the 'Cache' class. """


import random
import redis
import uuid
from typing import Union


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

    def store(
            self,
            data: Union[str, bytes, int, float]) -> str:
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)

        return random_key
