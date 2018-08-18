#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import time

from sanic import Blueprint
from sanic.response import html, json, text
from sanic.exceptions import NotFound

from hproxy.utils import logger
from hproxy.spider.proxy_tools import get_proxy_info, request_url_by_aiohttp

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
            'msg': 'Deleting error!',
        }
    return json(result)


@bp_api.route('/get')
async def api_get(request):
    valid = request.args.get('valid', 1)
    try:
        speed, res_dict = await get_random_proxy(request, valid)
        if speed is not None:
            result = {
                'status': 1,
                'info': res_dict,
                'msg': 'success',
                'speed': speed
            }
        else:
            result = {
                'status': -1,
                'msg': 'Searching error,please try again!',
            }
    except Exception as e:
        logger.exception(type='/get', message=str(e))
        result = {
            'status': -1,
            'msg': 'Searching error!',
        }
    return json(result)


@bp_api.route('/html')
async def api_html(request):
    url = request.args.get('url')
    # TODO
    ajax = request.args.get('ajax', 0)
    foreign = request.args.get('foreign', 0)
    if url:
        speed, res_dict = await get_random_proxy(request)
        try:
            proxy = res_dict.get('proxy')
            html_res = await request_url_by_aiohttp(url=url, proxy='http://' + proxy)
            if html_res:
                return json({
                    'status': 1,
                    'info': {
                        'html': html_res,
                        'proxy': proxy
                    },
                    'msg': 'success'
                })
            else:
                return json({
                    'status': -1,
                    'info': {
                        'proxy': proxy,
                        'details': proxy
                    },
                    'msg': 'Crawling failed!'
                })

        except:
            return json({
                'status': -1,
                'msg': 'Crawling failed!'
            })
    else:
        return json({
            'status': -1,
            'msg': 'URL is required'
        })


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
            'msg': 'Searching error!',
        }
    return json(result)


@bp_api.route("/valid/<proxy>")
async def api_valid(request, proxy):
    try:
        ip, port = str(proxy).split(':')
        start = time.time()
        is_ok = await get_proxy_info(ip, port)
        if is_ok:
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
                'msg': 'Invalid proxy!'
            }
    except Exception as e:
        result = {
            'status': -1,
            'msg': 'Deleting error!',
        }
    return json(result)


async def get_random_proxy(request, valid=1):
    try:
        db_client = request.app.db_client
        res = await db_client.get_random()
        if res:
            res_dict = list(res.values())[0]
            proxy = res_dict.get('proxy')
            ip, port = str(proxy).split(':')
            start = time.time()
            if valid == 0:
                return 0, res_dict
            else:
                is_ok = await get_proxy_info(ip, port)
                if is_ok:
                    speed = time.time() - start
                    return speed, res_dict
                else:
                    # Delete invalid proxy
                    await db_client.delete(proxy)
                    speed, res_dict = await get_random_proxy(request)
                    return speed, res_dict
        else:
            return None, None
    except Exception as e:
        return None, None
