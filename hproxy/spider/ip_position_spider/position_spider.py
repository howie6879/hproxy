#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
from hproxy.database import DatabaseSetting

from hproxy.spider.base_spider import ProxySpider
from hproxy.spider.ip_position_spider import PositionItem
from hproxy.spider.proxy_tools import request_url_by_aiohttp, get_proxy_info
from datetime import datetime

db_client = DatabaseSetting()

class PositionSpider(ProxySpider):
    """
    Fetch position from http://www.ip138.com/ips138.asp
    """
    spider_name = 'position'
    item = PositionItem

    async def get_position(self,ip):
        """
        Fetch http://www.ip138.com/ips138.asp
        :return:
        """
        kv = {'ip': ip}
        html = await request_url_by_aiohttp(url='http://www.ip138.com/ips138.asp',params=kv)
      #  print (html)
        if html:
            items_data = self.item.get_items(html=html)
            for item in items_data:
                dict =  (str(item.target_item).split('  '))
                print (dict)
                return dict
    @classmethod
    async def start(cls,ip):
        """Start a spider"""
        spider_instance = cls()
        spider_instance.logger.info(type='开始运行爬虫', message=spider_instance.spider_name + " 正在爬取中...")
        start = datetime.now()
        # asyncio.get_event_loop().run_until_complete(spider_instance.get_proxy())
        position = await spider_instance.get_position(ip)
        spider_instance.logger.info(type='爬虫运行结束',
                                    message='Time usage：{seconds}'.format(seconds=(datetime.now() - start)))
        return position


if __name__ == '__main__':
    import asyncio
    # Start
    asyncio.get_event_loop().run_until_complete(PositionSpider.start(ip = '120.36.255.208'))
