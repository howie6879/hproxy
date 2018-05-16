#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import os


class Config():
    """
    Basic config for hproxy
    """

    # Application config
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DB_TYPE = os.getenv('DB_TYPE', "redis")
    HOST = ['127.0.0.1:8001', '0.0.0.0:8001']
    START_SPIDER = int(os.getenv('START_SPIDER', '1'))
    TIMEZONE = 'Asia/Shanghai'
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    VAL_HOST = str(os.getenv('VAL_HOST', '0'))

    # scheduled task
    SCHEDULED_DICT = {
        'ver_interval': int(os.getenv('VER_INTERVAL', 10)),
        'spider_interval': int(os.getenv('SPIDER_INTERVAL', 60)),
    }

    # URL config
    TEST_URL = {
        'http': 'http://httpbin.org/get?show_env=1',
        'https': 'https://httpbin.org/get?show_env=1',
        'timeout': 5
    }
