#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import os


def load_config():
    """
    Load a config class
    """

    mode = os.environ.get('MODE', 'DEV')
    try:
        if mode == 'PRO':
            from .pro_config import ProConfig
            return ProConfig
        elif mode == 'DEV':
            from .dev_config import DevConfig
            return DevConfig
        else:
            from .dev_config import DevConfig
            return DevConfig
    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()
