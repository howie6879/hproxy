#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import asyncio
import os
import random

import uvloop

from functools import wraps
from urllib.parse import urlparse


def async_callback(func, **kwargs):
    """
    Call the asynchronous function
    :param func: a async function
    :param kwargs: params
    :return: result
    """
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(func(**kwargs))
    loop.run_until_complete(task)
    return task.result()


def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    return random.choice(_get_data('user_agents.txt', USER_AGENT))


def get_domain(url):
    """
    Get a domain from url
    :param url:
    :return: domain
    """
    domain = urlparse(url).netloc
    return domain


def _get_data(filename, default=''):
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(root_folder, filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except:
        data = [default]
    return data


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
