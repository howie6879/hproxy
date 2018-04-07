#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

import abc


class BaseDatabase(metaclass=abc.ABCMeta):
    """
    The class defines some functions that is necessary provided by RedisClient MemoryClient
    """

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def delete(self, *keys, **kwargs):
        """
        Delete one or more keys specified by ``keys``
        """
        pass

    @abc.abstractmethod
    def exists(self, field, **kwargs):
        """
        Return a boolean indicating whether key ``field`` exists
        """
        pass

    @abc.abstractmethod
    def get(self, field, default=None, **kwargs):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        pass

    @abc.abstractmethod
    def get_all(self, default=None, **kwargs):
        """
        Return all values
        """
        pass

    @abc.abstractmethod
    def get_random(self, default=None, **kwargs):
        """
        Return a random value
        """
        pass

    @abc.abstractmethod
    def insert(self, field, value={}, **kwargs):
        """
        insert the field
        """
        pass
