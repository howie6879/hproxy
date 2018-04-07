#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

from hproxy.spider.base_spider import Item, TextField, AttrField


class XCDLItem(Item):
    """Item for http://www.xicidaili.com/"""
    target_item = TextField(css_select='#ip_list tr')
    values = TextField(css_select='tr>td')

    def tal_values(self, values):
        if values and isinstance(values, list):
            try:
                res = (values[1].text, values[2].text)
                return res
            except:
                pass
