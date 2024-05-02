#!/usr/bin/env python3
"""uses the requests module to obtain the HTML
content of a particular URL and returns it.
"""
import requests
from functools import wraps
from typing import Callable
import redis


def count(method: Callable):
    """Function that count the call to requests"""
    red = redis.Redis()

    @wraps(method)
    def wrapped(url):
        """function that will count"""
        result = red.get(f"cached:{url}")
        if result:
            return result.decode('utf-8')
        else:
            red.incr(f"count:{url}")
            result = method(url)
            red.setex(f"cached:{url}", 10, result)
            return result

    return wrapped


@count
def get_page(url: str) -> str:
    """the module to obtain the html"""
    res = requests.get(url)
    return res.text
