#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

import random

from hproxy.database import BaseDatabase


class MemoryDatabase(BaseDatabase):
    _cache = {}

    def __init__(self, name='hproxy', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self._cache[self.name] = {}

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
            await self._delete(key)

    async def exists(self, field, **kwargs):
        """
        Return a boolean indicating whether key exists
        """
        return field in self._cache.get(self.name, {})

    async def get(self, field, default=None, **kwargs):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        return self._cache.get(self.name, {}).get(field, default)

    async def get_all(self, default=None, **kwargs):
        """
        Return all values
        """
        all_dict = self._cache.get(self.name, {})
        return all_dict if all_dict else default

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

    async def insert(self, field, value={}, **kwargs):
        """
        insert the value
        """
        try:
            self._cache.get(self.name, {})[field] = value
            return True
        except:
            return False

    async def _delete(self, key):
        return self._cache.get(self.name, {}).pop(key, 0)


if __name__ == '__main__':
    import asyncio

    memory_client = MemoryDatabase()

    print(asyncio.get_event_loop().run_until_complete(
        memory_client.insert(field='127.0.0.1:8001', value={'a': 1, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(
        memory_client.insert(field='127.0.0.1:8002', value={'a': 2, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(
        memory_client.insert(field='127.0.0.1:8003', value={'a': 3, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_all()))

    print(asyncio.get_event_loop().run_until_complete(memory_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_random()))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_all()))

    asyncio.get_event_loop().run_until_complete(memory_client.delete('127.0.0.1:8001'))
    print(asyncio.get_event_loop().run_until_complete(memory_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_all()))
