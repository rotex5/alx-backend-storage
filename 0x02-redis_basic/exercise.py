#!/usr/bin/env python3
"""
Redis basic
"""
import redis
from uuid import uuid4
from typing import Union


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
