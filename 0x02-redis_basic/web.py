#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable


redis_conn = redis.Redis()


def cache_expiring(time: int):
    """
    Decortator for counting how many times a request
    has been made
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(url: str) -> str:
            """ Wrapper for decorator functionality """
            cache_key = f"cached:{url}"
            cached_content = redis_conn.get(cache_key)
            if cached_content:
                return cached_content.decode("utf-8")

            response = func(url)
            redis_conn.setex(cache_key, time, response)
            return response
        return wrapper
    return decorator


def count_requests(func: Callable) -> Callable:
    """
    It uses the requests module to obtain the
    HTML content of a particular URL and returns it
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_conn.incr(count_key)
        return func(url)
    return wrapper


@cache_expiring(10)
@count_requests
def get_page(url: str) -> str:
    req = requests.get(url)
    return req.text
