#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import asyncio
import os

from importlib import import_module

from hproxy.config import CONFIG


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
    all_files = file_name()
    for spider in all_files:
        spider_module = import_module(
            "hproxy.spider.proxy_spider.{}".format(spider))
        await spider_module.start()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(spider_console())
