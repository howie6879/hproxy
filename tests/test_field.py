#!/usr/bin/env python
"""
 Created by howie.hu at 2018/4/24.
"""

import unittest

from lxml import etree

from hproxy.spider.base_spider import AttrField, TextField

HTML = """
<html>
    <head>
        <title>talonspider</title>
    </head>
    <body>¬
        <p>
            <a class="test_link" href="https://github.com/howie6879/talonspider">hello github.</a>
        </p>
    </body>
</html>
"""


class TestField(unittest.TestCase):
    def setUp(self):
        super(TestField, self).setUp()
        self.html = etree.HTML(HTML)

    def test_css_select(self):
        field = TextField(css_select="head title")
        value = field.extract_value(self.html)
        self.assertEqual(value, "talonspider")

    def test_xpath_select(self):
        field = TextField(xpath_select='/html/head/title')
        value = field.extract_value(self.html)
        self.assertEqual(value, "talonspider")

    def test_attr_field(self):
        attr_field = AttrField(css_select="p a.test_link", attr='href')
        value = attr_field.extract_value(self.html)
        self.assertEqual(value, "https://github.com/howie6879/talonspider")


if __name__ == '__main__':
    unittest.main()
