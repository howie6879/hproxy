#!/usr/bin/env python
"""
 Created by howie.hu at 07/04/2018.
"""
import asyncio
import unittest

from hproxy.database import DatabaseSetting
from hproxy.database.backends import MemoryDatabase


class Settings:
    """Global Settings"""
    db_setting = {
        'db_class': MemoryDatabase,
        'db_config': {
            'name': 'hproxy'
        }
    }


class TestMemoryDatabase(unittest.TestCase):
    def test_memory_client(self):
        memory_client = DatabaseSetting(settings=Settings)
        asyncio.get_event_loop().run_until_complete(memory_client.insert(field='127.0.0.1:8001'))
        res = asyncio.get_event_loop().run_until_complete(memory_client.get_random(field='127.0.0.1:8001'))
        assert res == {'127.0.0.1:8001': {}}


if __name__ == '__main__':
    unittest.main()
