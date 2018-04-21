#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from functools import wraps


def async_callback(func, **kwargs):
    """
    Call the asynchronous function
    :param func: a async function
    :param kwargs: params
    :return: result
    """
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(func(**kwargs))
    loop.run_until_complete(task)
    return task.result()


def singleton(cls):
    """
    A singleton created by using decorator
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance
