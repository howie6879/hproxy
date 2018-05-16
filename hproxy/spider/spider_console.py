#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import asyncio
import os
import sys
import time

sys.path.append('../../')

from importlib import import_module

from hproxy.config import CONFIG
from hproxy.utils import logger


def file_name(file_dir=os.path.join(CONFIG.BASE_DIR, 'spider/proxy_spider')):
    """
    Get spider class
    :param file_dir:
    :return:
    """
    all_files = []
    for file in os.listdir(file_dir):
        if file.endswith('_spider.py'):
            all_files.append(file.replace('.py', ''))
    return all_files


async def spider_console():
    start = time.time()
    all_files = file_name()
    tasks = []
    for spider in all_files:
        spider_module = import_module(
            "hproxy.spider.proxy_spider.{}".format(spider))
        tasks.append(asyncio.ensure_future(spider_module.start()))

    await asyncio.wait(tasks)
    logger.info(type="Spider finished!", message="Time costs: {0}".format(time.time() - start))


def crawl_proxy():
    asyncio.get_event_loop().run_until_complete(spider_console())


if __name__ == '__main__':
    crawl_proxy()
