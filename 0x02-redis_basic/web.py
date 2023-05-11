#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
import time
import redis
from functools import wraps

# Create a Redis client
redis_client = redis.Redis()


def cache_with_count(expiration_time):
    """
    Decorator counting how many times a URL is accessed
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            # Check if the URL is present in the cache
            cached_data = redis_client.get(url)
            if cached_data is not None:
                return cached_data.decode('utf-8')

            # URL not present in the cache, fetch it from the server
            response = requests.get(url)
            html_content = response.text

            # Store the result in the cache with the given expiration time
            redis_client.setex(url, expiration_time, html_content)

            # Track the number of times the URL was accessed
            redis_client.incr(f'count:{url}')

            return html_content
        return wrapper
    return decorator


@cache_with_count(10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL and return it
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    print(get_page("https://github.com/"))
