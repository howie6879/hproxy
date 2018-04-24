#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import os

from .config import Config


class DevConfig(Config):
    """
    DevConfig for hproxy
    """

    # Application config
    # memory or redis
    DB_TYPE = os.getenv('DB_TYPE', "redis")

    # Database config
    REDIS_DICT = dict(
        REDIS_ENDPOINT=os.getenv('REDIS_ENDPOINT', "localhost"),
        REDIS_PORT=int(os.getenv('REDIS_PORT', 6379)),
        REDIS_DB=int(os.getenv('REDIS_DB', 0)),
        REDIS_PASSWORD=os.getenv('REDIS_PASSWORD', None)
    )
