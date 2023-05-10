#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    Decorator func for counting how many times a function
    has been called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        wrapper for decorator functionality. Increments the
        call count for the method and returns its result.
        """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator func for storing the history of inputs and outputs
    for a method in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper for decorator functionality. Records the
        inputs and outputs of the method in Redis
        and returns its result.
        """

        inputs_key = method.__qualname__ + ":inputs"
        outputs_key = method.__qualname__ + ":outputs"

        input_data = str(args)
        output_data = str(method(self, *args, **kwargs))

        self._redis.rpush(inputs_key, input_data)
        self._redis.rpush(outputs_key, output_data)

        return output_data

    return wrapper


class Cache:
    """
    Class implementation of a cache
    """
    def __init__(self):
        """
        Initializes a cache instance with the given Redis
        connection. If no connection is provided, a new
        connection is created with default options.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis and returns a randomly
        generated key to retrieve it.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """ Returns the value associated with the given key from
        Redis, optionally transformed by the given function."""
        val = self._redis.get(key)
        if fn:
            val = fn(val)
        return val

    def get_str(self, key: str) -> str:
        """ Returns the string value associated with the
        given key from Redis."""
        val = self._redis.get(key)
        return val.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ Returns the integer value associated with the given
        key from Redis, or zero if the key is not present or
        the value is not a valid integer."""
        val = self._redis.get(key)
        try:
            val = int(val.decode("utf-8"))
        except Exception:
            val = 0
        return val
