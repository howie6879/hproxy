#!/usr/bin/env python
"""
 Created by howie.hu at 17/04/2018.
"""
import os
import sys
import time

import schedule

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hproxy.config import CONFIG
from hproxy.scheduler import refresh_proxy
from hproxy.spider.spider_console import crawl_proxy


def refresh_task(ver_interval, spider_interval):
    schedule.every(ver_interval).minutes.do(refresh_proxy)
    schedule.every(spider_interval).minutes.do(crawl_proxy)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__' and CONFIG.DB_TYPE != 'memory':
    crawl_proxy()
    ver_interval = CONFIG.SCHEDULED_DICT['ver_interval']
    spider_interval = CONFIG.SCHEDULED_DICT['spider_interval']
    refresh_task(ver_interval=ver_interval, spider_interval=spider_interval)
