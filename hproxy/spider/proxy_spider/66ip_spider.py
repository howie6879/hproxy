#!/usr/bin/env python
"""
 Created by howie.hu at 08/04/2018.
"""

from hproxy.database import DatabaseSetting

from hproxy.spider.base_spider import ProxySpider
from hproxy.spider.proxy_spider import SSIPItem
from hproxy.spider.proxy_tools import request_url_by_aiohttp, get_proxy_info

db_client = DatabaseSetting()


class SSIPSpider(ProxySpider):
    """
    Fetch proxies from http://www.66ip.cn/areaindex_1/1.html
    """
    spider_name = '66ip'
    item = SSIPItem

    async def get_proxy(self):

        for url in ['http://www.66ip.cn/areaindex_{}/1.html'.format(i) for i in range(1, 35)]:
            html = await request_url_by_aiohttp(url=url)
            if html:
                items_data = self.item.get_items(html=html)

                for each in items_data:
                    if each.values:
                        ip, port = each.values
                        isValid = get_proxy_info(ip, port)
                        if isValid:
                            # Save proxy
                            try:
                                await db_client.insert(field="{0}:{1}".format(ip, port))
                                self.logger.info(type='有效代理',
                                                 message="{0}: {1}:{2} 已存储".format(self.spider_name, ip, port))
                            except Exception as e:
                                self.logger.info(type='无效代理',
                                                 message="{0}: {1}:{2} 已丢弃".format(self.spider_name, ip, port))


async def start():
    """
    Start spider
    :return:
    """
    await SSIPSpider.start()


if __name__ == '__main__':
    import asyncio

    # Start
    asyncio.get_event_loop().run_until_complete(start())
