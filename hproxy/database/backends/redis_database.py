#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import aioredis
import random

from hproxy.database import BaseDatabase
from hproxy.database.decorator import dec_connector

try:
    from ujson import dumps as json_dumps
    from ujson import loads as json_loads
except:
    from json import dumps as json_dumps
    from json import loads as json_loads


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
            res = await self._client_conn.hgetall(self.name)
            all_dict = {key.decode('utf-8'): json_loads(value.decode('utf-8')) for key, value in res.items()}
        except Exception as e:
            all_dict = default
        return all_dict

    @dec_connector
    async def get_random(self, default=None, **kwargs):
        """
        Return a random value
        """
        all_dict = await self.get_all()
        if all_dict:
            key = random.choice(list(all_dict.keys()))
            return {
                key: all_dict[key]
            }
        else:
            return default

    @dec_connector
    async def insert(self, field, value={}, **kwargs):
        """
        insert the value
        """
        if isinstance(value, (list, dict)):
            value = json_dumps(value)
        return await self._client_conn.hset(key=self.name, field=field, value=value)

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

    print(asyncio.get_event_loop().run_until_complete(
        redis_client.insert(field='127.0.0.1:8001', value={'a': 1, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(
        redis_client.insert(field='127.0.0.1:8002', value={'a': 2, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(
        redis_client.insert(field='127.0.0.1:8003', value={'a': 3, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))

    print(asyncio.get_event_loop().run_until_complete(redis_client.get_random()))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get(field='127.0.0.1:8003')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))

    print(asyncio.get_event_loop().run_until_complete(redis_client.delete('127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))
