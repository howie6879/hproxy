#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sanic import Sanic
from sanic.response import redirect

from hproxy.config import CONFIG
from hproxy.database import DatabaseSetting
from hproxy.spider import spider_console
from hproxy.views import bp_api

app = Sanic(__name__)

if CONFIG.DB_TYPE == 'memory':
    app.add_task(spider_console())

app.blueprint(bp_api)
app.config.REQUEST_TIMEOUT = 600
app.static('/statics', CONFIG.BASE_DIR + '/statics/')


@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db_client = DatabaseSetting()


@app.middleware('request')
async def check_request(request):
    if CONFIG.VAL_HOST == '1':
        host = request.headers.get('host', None)
        if not host or host not in CONFIG.HOST:
            return redirect('http://www.baidu.com')


if __name__ == "__main__":
    app.run(host="127.0.0.1", workers=1, port=8001, debug=True)
