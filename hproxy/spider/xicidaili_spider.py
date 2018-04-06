#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import asyncio

from hproxy.database import DatabaseSetting
from hproxy.utils import async_callback, logger

from hproxy.spider.all_items import XCDLItem
from hproxy.spider.proxy_tools import request_url_by_aiohttp, get_proxy_info

db_client = DatabaseSetting()


def get_proxy():
    """
    Fetch proxies from http://www.xicidaili.com/
    :return:
    """
    html = async_callback(request_url_by_aiohttp, url='http://www.xicidaili.com/')
    items_data = XCDLItem.get_items(html=html)

    for each in items_data:
        if each.values:
            ip, port = each.values
            isValid = get_proxy_info(ip, port)
            if isValid:
                # Save proxy
                try:
                    asyncio.get_event_loop().run_until_complete(db_client.insert(field="{0}:{1}".format(ip, port)))
                    logger.info(type='有效代理', message="{0}:{1} 已存储".format(ip, port))
                except Exception as e:
                    logger.info(type='无效代理', message="{0}:{1} 已丢弃".format(ip, port))


if __name__ == '__main__':
    get_proxy()
