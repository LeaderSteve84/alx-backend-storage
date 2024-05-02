#!/usr/bin/env python3
"""0x02. Redis basic"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Function that Count the number of times a function is called"""
    key_d = method.__qualname__

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """Extra behaviour to function that will count"""
        self._redis.incr(key_d)
        return method(self, *args, **kwargs)
    return wrapped


def call_history(method: Callable) -> Callable:
    """Function that Store's the history of inputs and outputs"""
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """Extra behaviour to function that will count"""
        input_a = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_a)
        output_a = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_a)
        return output_a
    return wrapped


def replay(fn: Callable) -> None:
    """Function that display the history of calls"""
    red = redis.Redis()
    function_name = fn.__qualname__
    count = red.get(function_name)
    try:
        count = int(count.decode("utf-8"))
    except Exception:
        count = 0
    print(f"{function_name} was called {count} times:")
    inputs = red.lrange(f"{function_name}:inputs", 0, -1)
    outputs = red.lrange(f"{function_name}:outputs", 0, -1)
    for one, two in zip(inputs, outputs):
        try:
            one = one.decode('utf-8')
        except Exception:
            one = ""
        try:
            two = two.decode('utf-8')
        except Exception:
            two = ""
        print(f"{function_name}(*{one}) -> {two}")


class Cache:
    """class that implement cache strategy with redis"""
    def __init__(self):
        """Constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """function that Get a dat that will be saved"""
        key_d = str(uuid4())
        self._redis.set(key_d, data)
        return key_d

    def get(
            self,
            key_d: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """function that extract the information saved in redis"""
        value = self._redis.get(key_d)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key_d: str) -> str:
        """Fuction that parameterizes a value from redis to string"""
        value = self._redis.get(key_d)
        return value.decode("utf-8")

    def get_int(self, key_d: str) -> int:
        """function that Parameterizes a value from redis to int"""
        value = self._redis.get(key_d)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
