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


async def fetch(client, url, proxies):
    with async_timeout.timeout(15):
        try:
            headers = {'user-agent': get_random_user_agent()}
            async with client.get(url, headers=headers) as response:
                assert response.status == 200
                logger.info(type='抓取成功', message='Task url: {}'.format(response.url))
                try:
                    text = await response.text()
                except:
                    text = await response.read()
                return text
        except Exception as e:
            logger.exception(type='抓取失败', message=str(e))
            return None


async def request_url_by_aiohttp(url, proxies=None):
    """
    Request a url by aiohttp
    :param url:
    :param proxies:
    :return:
    """
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, proxies=proxies)
        return html if html else None


def get_domain(url):
    """
    Get a domain from url
    :param url:
    :return: domain
    """
    domain = urlparse(url).netloc
    return domain


def get_proxy_info(ip, port, getInfo=False):
    proxies = {
        "http": "http://{ip}:{port}".format(ip=ip, port=port),
        "https": "http://{ip}:{port}".format(ip=ip, port=port)
    }
    if getInfo:
        # TODO
        pass
    else:
        return valid_proxies(proxies)


def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    return random.choice(_get_data('base/user_agents.txt', USER_AGENT))


def valid_proxies(proxies):
    """
    Return all usable proxies without socket 4/5
    :param proxies: str
    :return: str
    """
    # TODO valid socket 4/5
    response = request_url_by_requests(url=CONFIG.TEST_URL['http'], proxies=proxies)
    # if not response:
    #     response = request_url_by_requests(url=CONFIG.TEST_URL['https'], proxies=proxies)
    if response:
        # content = response.content
        # charset = cchardet.detect(content)
        # text = content.decode(charset['encoding'])
        # response_json = json_loads(text)
        # print(response_json)
        return True
    else:
        return False


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


def valid_proxies_info(proxies):
    """
    Valid proxies info
    :param proxies:
    :return:
    """
    pass


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
    ip, port = '119.28.138.104', 3128
    proxies = {
        "http": "http://{ip}:{port}".format(ip=ip, port=port),
        "https": "http://{ip}:{port}".format(ip=ip, port=port)
    }
    print(valid_proxies(proxies))
