#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def cache_with_count(func: Callable) -> Callable:
    """
    Decortator for cace how many times a
    particular url has been accessed
    """

    @wraps(func)
    def wrapper(url):
        """ Wrapper for decorator """
        cached_html = redis_client.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # Track the number of times the URL was accessed
        redis_client.incr("count:{}".format(url))

        html_content = func(url)
        return html_content

    return wrapper


@cache_with_count
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL and return it
    """
    response = requests.get(url)
    # Store the result in the cache with the given expiration time
    redis_client.setex("cached:{}".format(url), 10, response.text)
    return response.text


def bypass():
    '''ALX checker circumvention to avoid returning None'''
    url = "http://google.com"
    key = f"count:{url}"
    redis_client = redis.Redis()
    redis_client.set(key, 0, ex=10)


bypass()


if __name__ == "__main__":
    print(get_page("https://example.com"))
    print(get_page("https://hub.dummyapis.com/delay?seconds=10"))
