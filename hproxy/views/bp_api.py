#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import time

from sanic import Blueprint
from sanic.response import html, json, text
from sanic.exceptions import NotFound

from hproxy.spider.proxy_tools import get_proxy_info

bp_api = Blueprint(name='bp_api', url_prefix='api')


@bp_api.route('/')
async def api_index(request):
    data = {
        'delete/:proxy': 'Delete a proxy',
        'get': 'Get an usable proxy',
        'list': 'List all proxies',
        'valid/:proxy': 'Valid a proxy'
    }
    return json(data)


@bp_api.route("/delete/<proxy>")
async def api_delete(request, proxy):
    db_client = request.app.db_client
    try:
        await db_client.delete(proxy)
        result = {
            'status': 1,
            'msg': 'success'
        }
    except Exception as e:
        result = {
            'status': -1,
            'msg': '删除出错',
        }
    return json(result)


@bp_api.route('/get')
async def api_get(request):
    valid = request.args.get('valid', 1)

    async def get_random_proxy(request):
        db_client = request.app.db_client
        res = await db_client.get_random()
        proxy = list(res.keys())[0]
        if proxy:
            ip, port = str(proxy).split(':')
            start = time.time()
            if valid == 0:
                return 0, proxy, res
            isOk = get_proxy_info(ip, port)
            if isOk:
                speed = time.time() - start
                return speed, proxy, res
            else:
                # Delete invalid proxy
                await db_client.delete(proxy)
                await get_random_proxy(request)
        else:
            return None, None, None

    try:
        speed, proxy, res = await get_random_proxy(request)
        if speed is not None:
            result = {
                'status': 1,
                'info': {
                    'proxy': proxy,
                    'details': res[proxy]
                },
                'msg': 'success',
                'speed': speed
            }
        else:
            result = {
                'status': -1,
                'msg': '查询失败，请重试',
            }
    except Exception as e:
        result = {
            'status': -1,
            'msg': '查询出错',
        }
    return json(result)


@bp_api.route('/list')
async def api_list(request):
    db_client = request.app.db_client
    try:
        all_proxies = await db_client.get_all()
        result = {
            'status': 1,
            'info': all_proxies,
            'msg': 'success'
        }
    except Exception as e:
        result = {
            'status': -1,
            'msg': '查询出错',
        }
    return json(result)


@bp_api.route("/valid/<proxy>")
async def api_valid(request, proxy):
    try:
        ip, port = str(proxy).split(':')
        start = time.time()
        isOk = get_proxy_info(ip, port)
        if isOk:
            speed = time.time() - start
            result = {
                'status': 1,
                'msg': 'success',
                'speed': speed
            }
        else:
            db_client = request.app.db_client
            await db_client.delete(proxy)
            result = {
                'status': 0,
                'msg': '代理失效'
            }
    except Exception as e:
        result = {
            'status': -1,
            'msg': '删除出错',
        }
    return json(result)
