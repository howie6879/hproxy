#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import aioredis
import random

from hproxy.database import BaseDatabase
from hproxy.database.decorator import dec_connector


class RedisDatabase(BaseDatabase):
    _db = {}
    _client_conn = None

    def __init__(self, host="127.0.0.1", port=6379, db=0, password=None, name='hproxy', **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.name = name

    @dec_connector
    async def delete(self, *keys, **kwargs):
        """
        Delete one or more keys specified by ``keys``
        """

        def gen_keys(keys):
            all_keys = []
            for key in keys:
                if isinstance(key, list):
                    all_keys += gen_keys(keys=key)
                else:
                    all_keys.append(key)
            return all_keys

        all_keys = gen_keys(keys)
        for key in all_keys:
            await self._client_conn.hdel(key=self.name, field=key)

    @dec_connector
    async def exists(self, field, **kwargs):
        """
        Return a boolean indicating whether key field exists
        """
        return await self._client_conn.hexists(key=self.name, field=field)

    @dec_connector
    async def get(self, field, default=None, **kwargs):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        return await self._client_conn.hget(self.name, field=field)

    @dec_connector
    async def get_all(self, default=None, **kwargs):
        """
        Return all values
        """
        try:
            all_values = await self._client_conn.hgetall(self.name)
            all_keys = [key.decode('utf-8') for key in all_values.keys()]
        except Exception as e:
            all_keys = default
        return all_keys

    @dec_connector
    async def get_random(self, default=None, **kwargs):
        """
        Return a random value
        """
        all_keys = await self.get_all()
        return random.choice(all_keys) if all_keys else default

    @dec_connector
    async def insert(self, field, **kwargs):
        """
        insert the value
        """
        return await self._client_conn.hincrby(key=self.name, field=field)

    async def _db_client(self, db=None):
        client = await aioredis.create_redis_pool(
            'redis://{host}:{port}/{cur_db}'.format(host=self.host, port=self.port, cur_db=db),
            password=self.password,
            minsize=5,
            maxsize=10)
        return client

    async def _connector(self, db=None):
        if db is None:
            db = self.db
        if db not in self._db:
            self._db[db] = self._client_conn = await self._db_client(db)
        return self._db[db]


if __name__ == '__main__':
    import asyncio

    redis_client = RedisDatabase()

    print(asyncio.get_event_loop().run_until_complete(redis_client.insert(field='1')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='1')))
    # print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))
    # print(asyncio.get_event_loop().run_until_complete(redis_client.get_random()))
    # print(asyncio.get_event_loop().run_until_complete(redis_client.get(field='127.0.0.1:8003')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))

    print(asyncio.get_event_loop().run_until_complete(redis_client.delete('1')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='1')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))
