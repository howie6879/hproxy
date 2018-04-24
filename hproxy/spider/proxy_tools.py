#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import os
import random

import aiohttp
import async_timeout
import requests

from urllib.parse import urlparse

from hproxy.config import CONFIG
from hproxy.utils import logger

try:
    from ujson import loads as json_loads
except:
    from json import loads as json_loads


async def fetch(client, url, proxy, timeout):
    with async_timeout.timeout(15):
        try:
            headers = {'user-agent': get_random_user_agent()}
            async with client.get(url, headers=headers, proxy=proxy, timeout=timeout) as response:
                assert response.status == 200
                logger.info(type='抓取成功', message='Task url: {}'.format(response.url))
                try:
                    text = await response.text()
                except:
                    text = await response.read()
                return text
        except Exception as e:
            logger.exception(type='请求失败', message=url)
            return None


async def request_url_by_aiohttp(url, proxy=None, timeout=15):
    """
    Request a url by aiohttp
    :param url:
    :param proxy:
    :return:
    """
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, proxy=proxy, timeout=timeout)
        return html if html else None


async def get_proxy_info(ip, port, getInfo=False):
    proxies = {
        "http": "http://{ip}:{port}".format(ip=ip, port=port),
        "https": "http://{ip}:{port}".format(ip=ip, port=port)
    }
    isOk, info = await valid_proxies(ip, port)
    if getInfo:
        return isOk, info
    else:
        return isOk


async def valid_proxies(ip, port):
    """
    Return all usable proxies without socket 4/5
    :param ip:
    :param port:
    :return:
    """
    # TODO valid socket 4/5
    # response = request_url_by_requests(url=CONFIG.TEST_URL['http'], proxies=proxies)
    proxy = "http://{ip}:{port}".format(ip=ip, port=port)
    html = await request_url_by_aiohttp(url=CONFIG.TEST_URL['http'], proxy=proxy, timeout=CONFIG.TEST_URL['timeout'])
    if html:
        try:
            res_json = json_loads(html)
            headers = res_json.get('headers', {})
            X_Forwarded_For = headers.get('X-Forwarded-For')
            Proxy_Connection = headers.get('Proxy-Connection')
            if X_Forwarded_For and ',' in X_Forwarded_For:
                types = 3
            elif Proxy_Connection:
                types = 2
            else:
                types = 1
            info = {
                'proxy': "{ip}:{port}".format(ip=ip, port=port),
                'types': types
            }
            return True, info
        except Exception as e:
            return False, None
    else:
        return False, None


def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    return random.choice(_get_data('base_spider/user_agents.txt', USER_AGENT))


def request_url_by_requests(url, proxies):
    """
    Request a url by requests
    :param url:
    :param proxies:
    :return:
    """
    headers = {
        'User-Agent': get_random_user_agent()
    }
    try:
        res = requests.get(url, headers=headers, timeout=CONFIG.TEST_URL['timeout'],
                           proxies=proxies)
        res.raise_for_status()
    except requests.exceptions.ConnectTimeout as e:
        logger.error(type='代理验证超时', message=proxies.get('http', ) + ' 请求 ' + url + ' 失败')
        res = None
    except Exception as e:
        logger.error(type='代理验证出错', message=proxies.get('http', ) + ' 请求 ' + url + ' 失败')
        res = None
    return res


def _get_data(filename, default=''):
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(root_folder, filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except:
        data = [default]
    return data


if __name__ == '__main__':
    import asyncio

    ip, port = '182.45.176.77', 6666
    proxies = {
        "http": "http://{ip}:{port}".format(ip=ip, port=port),
        "https": "https://{ip}:{port}".format(ip=ip, port=port)
    }

    proxy = "http://{ip}:{port}".format(ip=ip, port=port)

    print(asyncio.get_event_loop().run_until_complete(get_proxy_info(ip, port, getInfo=True)))
