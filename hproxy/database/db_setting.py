#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
from hproxy.utils import singleton
from hproxy.database.backends import MemoryDatabase


class Settings:
    """Global Settings"""
    db_setting = {
        'db_class': MemoryDatabase,
        'db_config': {
            'name': 'hproxy'
        }
    }

@singleton
class DatabaseSetting:
    """
    Database setting configuration
    db_dict provides the basic configuration of the database
        - db_class: such as MemoryDatabase RedisDatabase etc.
        - db_config: basic configuration, just like redis's host port db password etc.
    """
    db_setting = Settings.db_setting

    def __init__(self, settings=Settings):
        self.db_setting = getattr(settings, 'db_setting', self.db_setting)
        if not isinstance(self.db_setting.get('db_config'), dict):
            raise ValueError("Key db_config must be a dict")
        self.instance = self.db_setting['db_class'](**self.db_setting['db_config'])

    async def delete(self, *keys, **kwargs):
        """
        Delete one or more keys specified by ``keys``
        """
        try:
            await self.instance.delete(*keys, **kwargs)
            return True
        except:
            return False

    async def exists(self, field, **kwargs):
        """
        Return a boolean indicating whether key exists
        """
        return await self.instance.exists(field, **kwargs)

    async def get(self, field, default=None, **kwargs):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        return await self.instance.get(field, default=default, **kwargs)

    async def get_all(self, default=None, **kwargs):
        """
        Return all values
        """
        return await self.instance.get_all(default=default, **kwargs)

    async def get_random(self, default=None, **kwargs):
        """
        Return a random value
        """
        return await self.instance.get_random(default=default, **kwargs)

    async def insert(self, field, value={}, **kwargs):
        """
        insert the value
        """
        return await self.instance.insert(field, value=value, **kwargs)


if __name__ == '__main__':
    import asyncio

    memory_client = DatabaseSetting()

    print(asyncio.get_event_loop().run_until_complete(
        memory_client.insert(field='127.0.0.1:8001', value={'a': 1, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(memory_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_random()))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_all()))

    asyncio.get_event_loop().run_until_complete(memory_client.delete('127.0.0.1:8001'))
    print(asyncio.get_event_loop().run_until_complete(memory_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_all()))

    # redis
    from hproxy.config import CONFIG
    from hproxy.database.backends import RedisDatabase

    print('Redis =================')


    class Settings:
        """Global Settings"""
        db_setting = {
            'db_class': RedisDatabase,
            'db_config': {
                'host': CONFIG.REDIS_DICT['REDIS_ENDPOINT'],
                'port': CONFIG.REDIS_DICT['REDIS_PORT'],
                'db': CONFIG.REDIS_DICT['REDIS_DB'],
                'password': CONFIG.REDIS_DICT['REDIS_PASSWORD'],
                'name': 'hproxy'
            }}


    print(Settings.db_setting)

    redis_client = DatabaseSetting(settings=Settings)

    print(asyncio.get_event_loop().run_until_complete(
        redis_client.insert(field='127.0.0.1:8001', value={'a': 1, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))

    print(asyncio.get_event_loop().run_until_complete(redis_client.get_random()))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))

    print(asyncio.get_event_loop().run_until_complete(redis_client.delete('127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))
