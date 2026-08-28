#!/usr/bin/env python3
""" Tasks - Redis """

import redis
from typing import Union, Optional, Callable
from uuid import uuid4, UUID
from functools import wraps

class Cache:
    """ Class for implementing a Cache """

    def __init__(self):
        """ Constructor Method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a
        random key and return the key.
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)

        return random_key
