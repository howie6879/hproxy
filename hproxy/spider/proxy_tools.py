#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import aiofiles
import aiohttp
import async_timeout
import os
import random
import requests

from urllib.parse import urlparse

from hproxy.config import CONFIG
from hproxy.utils import logger

try:
    from ujson import loads as json_loads
except:
    from json import loads as json_loads


async def fetch(client, url, proxy, params, timeout=15):
    with async_timeout.timeout(timeout):
        try:
            headers = {'user-agent': await get_random_user_agent()}
            async with client.get(url, headers=headers, proxy=proxy, params=params, timeout=timeout) as response:
                assert response.status == 200
                logger.info(type='Request success!', message='Task url: {}'.format(response.url))
                try:
                    text = await response.text()
                except:
                    text = await response.read()
                return text
        except Exception as e:
            logger.exception(type='Request failed!', message=url)
            return None


async def request_url_by_aiohttp(url, proxy=None, params={}, timeout=15):
    """
    Request a url by aiohttp
    :param url:
    :param proxy:
    :return:
    """
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, proxy=proxy, params=params, timeout=timeout)
        return html if html else None


async def get_proxy_info(ip, port, get_info=False):
    proxies = {
        "http": "http://{ip}:{port}".format(ip=ip, port=port),
        "https": "http://{ip}:{port}".format(ip=ip, port=port)
    }
    is_ok, info = await valid_proxies(ip, port)
    if get_info:
        return is_ok, info
    else:
        return is_ok


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


async def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    return random.choice(await _get_data('base_spider/user_agents.txt', USER_AGENT))


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
        logger.error(type='Request timeout!', message=proxies.get('http', ) + ' Request ' + url + ' failed')
        res = None
    except Exception as e:
        logger.error(type='Request failed!', message=proxies.get('http', ) + ' Request ' + url + ' failed')
        res = None
    return res


async def _get_data(filename, default=''):
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(root_folder, filename)
    try:
        async with aiofiles.open(user_agents_file, mode='r') as f:
            data = [_.strip() for _ in await f.readlines()]
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

    print(asyncio.get_event_loop().run_until_complete(get_random_user_agent()))

    print(asyncio.get_event_loop().run_until_complete(get_proxy_info(ip, port, get_info=True)))
