#!/usr/bin/env python3
"""
Redis basic
"""
import redis
from uuid import uuid4
from typing import Union, Optional, Callable


class Cache:
    """
    Class implementation of a cache
    """
    def __init__(self):
        """Initaillizing cache variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ return generated random key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """ returns original data """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ Parameterizes cache.get with the correct
        converion from redis value to str """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ Parameterizes chache.get with the correct
        conversion from redis value to int """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
