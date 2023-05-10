#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from typing import Union, Optional, Callable


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
