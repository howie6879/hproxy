#!/usr/bin/env python
"""
 Created by howie.hu at 08/04/2018.
"""
import asyncio
import sys
import time

sys.path.append('../../')

from hproxy.database import DatabaseSetting
from hproxy.utils import logger
from hproxy.spider.proxy_tools import get_proxy_info

db_client = DatabaseSetting()


async def valid_proxies():
    all_res = await db_client.get_all()
    start = time.time()
    tasks = []
    if all_res:
        for each in all_res.keys():
            tasks.append(asyncio.ensure_future(valid_proxy(each, nums=1)))
    done_list, pending_list = await asyncio.wait(tasks)
    good_nums = 0
    for task in done_list:
        if task.result():
            good_nums += 1

    logger.info(type="Refresh finished", message="Refresh finished ，total proxy num : {0} - valid proxy num : {1} ,Time costs : {2}".format(
        len(tasks),
        good_nums,
        time.time() - start))


async def valid_proxy(proxy, nums=1):
    if nums > 5:
        await db_client.delete(proxy)
        logger.error(type='Invalid proxy', message="{0} had been abandoned".format(proxy))
        return False
    else:
        ip, port = proxy.split(':')
        is_ok = await  get_proxy_info(ip, port)
        if not is_ok:
            logger.error(type='Invalid proxy', message="{0}：retry times =  {1}".format(proxy, nums))
            res = await valid_proxy(proxy, nums=nums + 1)
            return res
        else:
            logger.info(type='Valid proxy', message="{0} is valid".format(proxy))
            return True


def refresh_proxy():
    asyncio.get_event_loop().run_until_complete(valid_proxies())


if __name__ == '__main__':
    refresh_proxy()
