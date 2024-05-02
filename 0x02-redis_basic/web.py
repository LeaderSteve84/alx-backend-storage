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
        red.incr(f"count:{url}")
        expn_count = red.get(f"cached:{url}")
        if expn_count:
            return expn_count.decode('utf-8')
        html = method(url)
        red.setex(f"cached:{url}", 10, html)
        return html

    return wrapped


@count
def get_page(url: str) -> str:
    """the module to obtain the html"""
    return requests.get(url).text
