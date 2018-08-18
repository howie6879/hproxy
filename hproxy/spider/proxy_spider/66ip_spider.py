#!/usr/bin/env python
"""
 Created by howie.hu at 08/04/2018.
"""

import asyncio
import time

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
        """
        Fetch proxies from http://www.66ip.cn
        :return:
        """
        start = time.time()
        tasks = []
        for url in ['http://www.66ip.cn/areaindex_{}/1.html'.format(i) for i in range(1, 35)]:

            html = await request_url_by_aiohttp(url=url)
            if html:
                items_data = self.item.get_items(html=html)

                for item_data in items_data:
                    if item_data.values:
                        tasks.append(asyncio.ensure_future(self.save_proxy(item_data.values)))

        good_nums = 0
        if tasks:
            done_list, pending_list = await asyncio.wait(tasks)
            for task in done_list:
                if task.result():
                    good_nums += 1

        self.logger.info(type="Spider finished!",
                         message="Crawling {0} finished,total proxy num : {1}  - valid proxy num ：{2}，Time costs ：{3}".format(
                             self.spider_name,
                             len(tasks),
                             good_nums,
                             time.time() - start))

    async def save_proxy(self, ip_info):
        """
        Save proxy
        :param ip_info: (0.0.0.0, 8080)
        :return:
        """
        ip, port = ip_info
        is_ok, info = await get_proxy_info(ip, port, get_info=True)
        if is_ok:
            # Save proxy
            try:
                await db_client.insert(field="{0}:{1}".format(ip, port), value=info)
                self.logger.info(type='Valid proxy',
                                 message="{0}: {1}:{2} had been saved".format(self.spider_name, ip, port))
                return True
            except Exception as e:
                self.logger.info(type='Invalid proxy',
                                 message="{0}: {1}:{2} had been saved".format(self.spider_name, ip, port))
                return False
        return False


async def start():
    """
    Start spider
    :return:
    """
    await SSIPSpider.start()


if __name__ == '__main__':
    # Start
    asyncio.get_event_loop().run_until_complete(start())
