#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

from functools import wraps


def dec_connector(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self._client_conn is None:
            self._client_conn = await self._connector()

        return await func(self, *args, **kwargs)

    return wrapper
