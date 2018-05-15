#!/usr/bin/env python
"""
 Created by howie.hu at 07/04/2018.
"""
from datetime import datetime

from hproxy.utils import logger as hproxy_logger


class ProxySpider():
    """
    ProxySpider
    """
    spider_name = ''
    item = None
    logger = hproxy_logger

    def __init__(self):
        if not getattr(self, 'spider_name', None):
            raise ValueError('Spider must have a spider_name')
        if not getattr(self, 'item', None):
            raise ValueError('Spider must have a item')
        setattr(self, 'spider_name', self.spider_name)
        setattr(self, 'item', self.item)
        setattr(self, 'logger', self.logger)

    async def get_proxy(self):
        """It is a necessary method"""
        raise NotImplementedError

    async def save_proxy(self, ip_info):
        """It is a necessary method"""
        raise NotImplementedError

    @classmethod
    async def start(cls):
        """Start a spider"""
        spider_instance = cls()
        spider_instance.logger.info(type='Spider started', message=spider_instance.spider_name + " Crawling...")
        start = datetime.now()
        # asyncio.get_event_loop().run_until_complete(spider_instance.get_proxy())
        await spider_instance.get_proxy()
        spider_instance.logger.info(type='Spider finished',
                                    message='Time usage：{seconds}'.format(seconds=(datetime.now() - start)))
