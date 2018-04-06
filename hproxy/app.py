#!/usr/bin/env python
"""
 Created by howie.hu at 06/04/2018.
"""
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

from sanic import Sanic
from sanic.response import redirect

from hproxy.config import CONFIG
from hproxy.database import DatabaseSetting
from hproxy.views import bp_api

app = Sanic(__name__)

app.blueprint(bp_api)
app.config.REQUEST_TIMEOUT = 600
app.static('/statics', CONFIG.BASE_DIR + '/statics/')


@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db_client = DatabaseSetting()


@app.middleware('request')
async def check_request(request):
    host = request.headers.get('host', None)
    if not host or host not in CONFIG.HOST:
        return redirect('http://www.baidu.com')


if __name__ == "__main__":
    app.run(host="127.0.0.1", workers=1, port=8001, debug=True)
