#!/usr/bin/env python
"""
 Created by howie.hu at 08/04/2018.
"""
import asyncio
import sys
import time

import schedule

sys.path.append('../../')

from hproxy.database import DatabaseSetting
from hproxy.utils import logger
from hproxy.spider.proxy_tools import get_proxy_info

db_client = DatabaseSetting()


async def valid_proxies():
    all_res = await db_client.get_all()
    if all_res:
        for each in all_res.keys():
            await valid_proxy(each, nums=1)


async def valid_proxy(proxy, nums=1):
    if nums > 3:
        await db_client.delete(proxy)
        logger.error(type='无效代理', message="{0} 已丢弃".format(proxy))
    else:
        ip, port = proxy.split(':')
        isOk = await  get_proxy_info(ip, port)
        if not isOk:
            logger.error(type='无效代理', message="{0}：第 {1} 次重试".format(proxy, nums))
            await valid_proxy(proxy, nums=nums + 1)
        else:
            logger.info(type='有效代理', message="{0} 有效".format(proxy))


def refresh():
    asyncio.get_event_loop().run_until_complete(valid_proxies())


schedule.every(60).minutes.do(refresh)

while True:
    schedule.run_pending()
    time.sleep(1)
