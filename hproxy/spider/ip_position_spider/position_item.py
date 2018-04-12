#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

from hproxy.spider.base_spider import Item, TextField, AttrField


class PositionItem(Item):
    """Item for http://www.ip138.com/ips138.asp"""
    target_item = TextField(css_select='ul.ul1')
    def tal_target_item(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])
