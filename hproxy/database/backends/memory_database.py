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
        all_keys = self._cache.get(self.name, {}).keys()
        return list(all_keys) if all_keys else default

    async def get_random(self, default=None, **kwargs):
        """
        Return a random value
        """
        all_keys = await self.get_all()
        return random.choice(all_keys) if all_keys else default

    async def insert(self, field, **kwargs):
        """
        insert the value
        """
        try:
            self._cache.get(self.name, {})[field] = self._cache.get(self.name, {}).get(field, 0) + 1
            return True
        except:
            return False

    async def _delete(self, key):
        return self._cache.get(self.name, {}).pop(key, 0)


if __name__ == '__main__':
    import asyncio

    memory_client = MemoryDatabase()

    print(asyncio.get_event_loop().run_until_complete(memory_client.insert(field='1')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.insert(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.insert(field='127.0.0.1:8002')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.insert(field='127.0.0.1:8003')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.exists(field='1')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_random()))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_all()))

    asyncio.get_event_loop().run_until_complete(memory_client.delete('1'))
    print(asyncio.get_event_loop().run_until_complete(memory_client.exists(field='1')))
    print(asyncio.get_event_loop().run_until_complete(memory_client.get_all()))
