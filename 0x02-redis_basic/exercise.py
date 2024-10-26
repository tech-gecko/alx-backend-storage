#!/usr/bin/env python3
""" Module containing the 'Cache' class. """


import redis
import uuid
from functools import wraps
from typing import Any, Callable, Optional, Union


def call_history(method: Callable) -> Callable:
    """ Stores the history of inputs and outputs for a particular function. """
    @wraps(method)
    def wrapper(self, *args) -> Any:
        """ Invokes the given method after storing the history of inputs and outputs. """
        output = method(self, *args)

        self._redis.rpush("{}:inputs".format(method.__qualname__), str(args))
        self._redis.rpush("{}:outputs".format(method.__qualname__), output)
        return output

    return wrapper

def count_calls(method: Callable) -> Callable:
    """ Increases call count every time method is called. """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ Invokes the given method after incrementing its call counter. """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper

def replay(method: Callable) -> None:
    """ Displays the history of calls of a particular function. """
    redis_instance = method.__self__._redis  # Access the Redis instance
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    # Get the number of calls from Redis
    call_count = redis_instance.llen(inputs_key)
    print(f"{method.__qualname__} was called {call_count} times:")

    # Retrieve inputs and outputs from Redis
    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    # Display each call with its input and output
    for input_value, output_value in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_value.decode('utf-8')}) -> {output_value.decode('utf-8')}")


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

    @call_history
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
