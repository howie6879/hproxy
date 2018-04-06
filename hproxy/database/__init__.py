#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
from .base_database import BaseDatabase
from .db_setting import DatabaseSetting
from hproxy.config import CONFIG


def load_settings():
    from .db_setting import Settings

    if CONFIG.DB_TYPE == 'redis':
        from .backends import RedisDatabase
        Settings.db_setting = {
            'db_class': RedisDatabase,
            'db_config': {
                'host': CONFIG.REDIS_DICT['REDIS_ENDPOINT'],
                'port': CONFIG.REDIS_DICT['REDIS_PORT'],
                'db': CONFIG.REDIS_DICT['REDIS_DB'],
                'password': CONFIG.REDIS_DICT['REDIS_PASSWORD'],
                'name': 'hproxy'
            }
        }
    return Settings


Settings = load_settings()
