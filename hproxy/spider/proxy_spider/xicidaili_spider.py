#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

import asyncio
import time

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
        start = time.time()
        html = await request_url_by_aiohttp(url='http://www.xicidaili.com/')
        if html:
            items_data = self.item.get_items(html=html)
            tasks = []
            for item_data in items_data:
                if item_data.values:
                    tasks.append(asyncio.ensure_future(self.save_proxy(item_data.values)))

            done_list, pending_list = await asyncio.wait(tasks)
            good_nums = 0
            for task in done_list:
                if task.result():
                    good_nums += 1
            self.logger.info(type="爬虫执行结束", message="爬虫：{0} 执行结束，获取代理{1}个 - 有效代理：{2}个，用时：{3}".format(
                self.spider_name,
                len(tasks),
                good_nums,
                time.time() - start))
        else:
            self.logger.info(type="爬虫执行失败", message="爬虫：{0} 执行结束，用时：{1}".format(self.spider_name, time.time() - start))

    async def save_proxy(self, ip_info):
        """
        Save proxy
        :param ip_info: (0.0.0.0, 8080)
        :return:
        """
        ip, port = ip_info
        isOk, info = await get_proxy_info(ip, port, getInfo=True)
        if isOk:
            # Save proxy
            try:
                await db_client.insert(field="{0}:{1}".format(ip, port), value=info)
                self.logger.info(type='有效代理', message="{0}: {1}:{2} 已存储".format(self.spider_name, ip, port))
                return True
            except Exception as e:
                self.logger.info(type='无效代理', message="{0}: {1}:{2} 已丢弃".format(self.spider_name, ip, port))
                return False
        return False


async def start():
    """
    Start spider
    :return:
    """
    await XCDLSpider.start()


if __name__ == '__main__':
    # Start
    asyncio.get_event_loop().run_until_complete(start())
