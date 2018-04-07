#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import asyncio

from hproxy.database import DatabaseSetting

from hproxy.spider.base_spider import ProxySpider
from hproxy.spider.proxy_spider import XCDLItem
from hproxy.spider.proxy_tools import request_url_by_aiohttp, get_proxy_info

db_client = DatabaseSetting()


class XCDLSpider(ProxySpider):
    """
    Fetch proxies from http://www.xicidaili.com/
    """
    spider_name = 'xicidaili'
    item = XCDLItem

    async def get_proxy(self):
        """
        Fetch proxies from http://www.xicidaili.com/
        :return:
        """
        html = await request_url_by_aiohttp(url='http://www.xicidaili.com/')
        items_data = XCDLItem.get_items(html=html)

        for each in items_data:
            if each.values:
                ip, port = each.values
                isValid = get_proxy_info(ip, port)
                if isValid:
                    # Save proxy
                    try:
                        await db_client.insert(field="{0}:{1}".format(ip, port))
                        self.logger.info(type='有效代理', message="{0}:{1} 已存储".format(ip, port))
                    except Exception as e:
                        self.logger.info(type='无效代理', message="{0}:{1} 已丢弃".format(ip, port))


async def start():
    """
    Start spider
    :return:
    """
    await XCDLSpider.start()


if __name__ == '__main__':
    # Start
    asyncio.get_event_loop().run_until_complete(start())
