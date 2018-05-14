#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

from hproxy.spider.base_spider import Item, TextField, AttrField


class SSIPItem(Item):
    """Item for http://www.66ip.cn/index.html"""
    target_item = TextField(css_select='#footer table tr')
    values = TextField(css_select='tr>td')

    def tal_values(self, values):
        if values and isinstance(values, list):
            try:
                if str(values[1].text).isdigit():
                    res = (values[0].text, values[1].text)
                    return res
            except:
                pass
        return None


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


class MimvpItem(Item):
    """Item for http://www.66ip.cn/index.html"""
    target_item = TextField(css_select='#footer table tr')
    values = TextField(css_select='tr>td')

    def tal_values(self, values):
        if values and isinstance(values, list):
            try:
                if str(values[1].text).isdigit():
                    res = (values[0].text, values[1].text)
                    return res
            except:
                pass
        return None
