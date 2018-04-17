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


def refresh_task(interval):
    schedule.every(interval).minutes.do(refresh_proxy)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    interval = CONFIG.SCHEDULED_DICT['ver_interval']
    refresh_task(interval=interval)
