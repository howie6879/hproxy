#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import cchardet
import requests

from lxml import etree

from hproxy.spider.base_spider import BaseField
from hproxy.spider.proxy_tools import get_random_user_agent


def with_metaclass(meta):
    return meta("Talospider", (object,), {})


class ItemMeta(type):
    """
    Metaclass for a talospider item
    Token from https://github.com/howie6879/talospider
    """

    def __new__(cls, name, bases, attrs):
        _fields = dict({(field_name, attrs.pop(field_name)) for field_name, object in list(attrs.items()) if
                        isinstance(object, BaseField)})
        attrs['_fields'] = _fields
        new_class = super(ItemMeta, cls).__new__(cls, name, bases, attrs)
        return new_class


class Item(with_metaclass(ItemMeta)):
    """
    Item class for each item
    """

    def __init__(self, html):
        if html is None or not isinstance(html, etree._Element):
            raise ValueError("etree._Element is expected")
        for field_name, field_value in self._fields.items():
            get_field = getattr(self, 'tal_%s' % field_name, None)
            value = field_value.extract_value(html) if isinstance(field_value, BaseField) else field_value
            if get_field:
                value = get_field(value)
            setattr(self, field_name, value)

    @classmethod
    def _get_html(cls, html, url, html_etree, params, **kwargs):
        if html:
            html = etree.HTML(html)
        elif url:
            if not kwargs.get('headers', None):
                kwargs['headers'] = {
                    "User-Agent": get_random_user_agent()
                }
            response = requests.get(url, params, **kwargs)
            response.raise_for_status()
            content = response.content
            charset = cchardet.detect(content)
            text = content.decode(charset['encoding'])
            html = etree.HTML(text)
        elif html_etree is not None:
            return html_etree
        else:
            raise ValueError("html(url or html_etree) is expected")
        return html

    @classmethod
    def get_item(cls, html='', url='', html_etree=None, params=None, **kwargs):
        html = cls._get_html(html, url, html_etree, params=params, **kwargs)
        item = {}
        ins_item = cls(html=html)
        for i in cls._fields.keys():
            item[i] = getattr(ins_item, i)
        return item

    @classmethod
    def get_items(cls, html='', url='', html_etree=None, params=None, **kwargs):
        html = cls._get_html(html, url, html_etree, params=params, **kwargs)
        items_field = cls._fields.get('target_item', None)
        if items_field:
            items = items_field.extract_value(html, is_source=True)
            return [cls(html=i) for i in items]
        else:
            raise ValueError("target_item is expected")
