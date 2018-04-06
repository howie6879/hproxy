#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""

from sanic import Blueprint
from sanic.response import html, json, text
from sanic.exceptions import NotFound

bp_api = Blueprint(name='bp_api', url_prefix='api')


@bp_api.route('/')
async def api_index(request):
    data = {
        'delete/:proxy': 'Delete a proxy',
        'get': 'Get an usable proxy',
        'list': 'List all proxies',
    }
    return json(data)
