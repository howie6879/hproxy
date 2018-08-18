## Hproxy - Asynchronous IP proxy pool

[![Build Status](https://travis-ci.org/howie6879/hproxy.svg?branch=master)](https://travis-ci.org/howie6879/hproxy) [![Python](https://img.shields.io/badge/python-3.6%2B-orange.svg)](https://github.com/howie6879/hproxy) [![license](https://img.shields.io/github/license/howie6879/hproxy.svg)](https://github.com/howie6879/hproxy) 

Hproxy aims to make getting proxy as convenient as possible.

- Demo: https://hproxy.htmlhelper.org/api
- Introduction：[中文](./ZH_README.md) | [English](./README.md)

### Overview

The hproxy requires Python3.6+,and it use `Sanic` to build asynchronous HTTP service and `aiohttp` to crawl proxy data asynchronously.

``` shell
git clone https://github.com/howie6879/hproxy.git
cd hproxy
pip install pipenv

# It should be noted that Python3.6 is required if you were in a virtual environment.
# Install Dependencies
pipenv install

# Start Crawler
cd hproxy
python server.py

# Start Crawling
python /hproxy/hproxy/spider/spider_console.py

```

The precondition to use hproxy is that Redis must has been installed because hproxy user Redis as default data storage mode,
and the specific configuration is in the `config` directory.

``` python
# Database config
REDIS_DICT = dict(
    REDIS_ENDPOINT=os.getenv('REDIS_ENDPOINT', "localhost"),
    REDIS_PORT=os.getenv('REDIS_PORT', 6379),
    REDIS_DB=os.getenv('REDIS_DB', 0),
    REDIS_PASSWORD=os.getenv('REDIS_PASSWORD', None)
)
DB_TYPE = 'redis'
```

If you want to use `Memory` in machine,you just need to change the value of `DB_TYPE` from `redis`
to `memory` in `config` as following.

It should be noted that the data saved in `Memory` will be lost when the service terminated if you use the `memory` mode,
so the `redis` mode is more recommended to keep the data.

If you want to use other mode,you just need to expand it referring to the coding standards in [BaseDatabase](https://github.com/howie6879/hproxy/blob/master/hproxy/database/base_database.py)

### Features

- [x] Multiple Data Storage Mode, Easy to expand:
    - [DatabaseSetting](https://github.com/howie6879/hproxy/blob/master/hproxy/database/db_setting.py)
    - [Memory](https://github.com/howie6879/hproxy/blob/master/hproxy/database/backends/memory_database.py)
    - [Redis](https://github.com/howie6879/hproxy/blob/master/hproxy/database/backends/redis_database.py)


- [x] Customize Crawling Components,Easy To Expand，Unity Code Style:
    - [Field](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base/field.py)
    - [Item](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base/item.py)

- [x] Provide API To Get Proxy,Visit `127.0.0.1:8001/api`
    - 'delete/:proxy': delete proxy
    - 'get': get a proxy randomly
    - 'list': list all proxies
    - ...

- [x] Provide crawling HTML source code service by a random proxy  from the proxy pool
- [x] Crawling,updating,and auto verifying at a regular time
- [ ] Get accurate information of the proxy,such as type of the proxy,protocol,position and so on

### Description of The Function

#### Obtaining proxy

The spider script are all in the [spider](https://github.com/howie6879/hproxy/tree/master/hproxy/spider) directory.You can easily expand the [spider/proxy_spider](https://github.com/howie6879/hproxy/tree/master/hproxy/spider/proxy_spider) which includes many spider towards different agency websites referring to the coding standard in [/spider/base_spider/proxy_spider.py](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base_spider/proxy_spider.py)

Execute [spider_console.py](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/spider_console.py) to start all the spider scripts.If you want to expand,you just need to add function named in standard but not new script. 

Run the following command to run the specific script like `xicidaili`.

``` shell
cd hproxy/hproxy/spider/proxy_spider/
python xicidaili_spider.py

# The process of verifying 100 proxies Asynchronously would finish in 5 seconds,because the proxy timeout is 5 seconds. 
# But in Synchronous way,it's unpredictable.
# 2018/04/14 13:42:32 [Crawling finished  ] OK. Crawling xicidaili finished,get 100 proxies - Invalid proxy num:8,cost 5.384464740753174 seconds
```

#### Proxy Verification

You can run the [valid_proxy.py](https://github.com/howie6879/hproxy/master/hproxy/scheduler/valid_proxy.py) to verify whether the proxies are available automatically or manually. 
In an automatic way, hproxy will verify all the proxies per hour,and those which is verified failed over 5 times will be abandoned.
In an manual way, you can run the following commands.


``` shell
cd hproxy/hproxy/scheduler/
python valid_proxy.py
```

#### Interface

| Route                                 | Description                                                         |
| :------------------------------------ | :----------------------------------------------------------- |
| delete/:proxy                         | Delete a proxy                                               |
| get                                   | Return a random proxy @param valid=1,continuously verify the return proxy until it's valid|
| list                                  | List all proxies without verification                               |
| valid/:proxy                          | Verify a proxy                                              |
| html?url=''&ajax=0&foreign=0          | Select a random proxy and request                                    |

``` json
// URL:http://127.0.0.1:8001/api/get?valid=1
// Description:Return successfully! If the value of the param 'valid' which is set to 1 as default is equal to 1,it will also return the value of param 'speed'.
// types 1:Elite 2:Anonymous  3:Transparent
{
    "status": 1,
    "info": {
        "proxy": "101.37.79.125:3128",
        "types": 3
    },
    "msg": "success",
    "speed": 2.4909408092
}
// URL:http://127.0.0.1:8001/api/list
//List all proxies without verification   
{
    "status": 1,
    "info": {
        "180.168.184.179:53128": {
            "proxy": "180.168.184.179:53128",
            "types": 3
        },
        "101.37.79.125:3128": {
            "proxy": "101.37.79.125:3128",
            "types": 3
        }
    },
    "msg": "success"
}
// URL:http://127.0.0.1:8001/api/delete/171.39.45.6:8123
{
    "status": 1,
    "msg": "success"
}
// URL:http://127.0.0.1:8001/api/valid/183.159.91.75:18118
{
    "status": 1,
    "msg": "success",
    "speed": 0.3361008167
}
// URL:http://127.0.0.1:8001/api/html?url=https://www.v2ex.com
// Crawing v2ex and get a random proxy.
{
    "status": 1,
    "info": {
        "html": "html source code",
        "proxy": "120.77.254.116:3128"
    },
    "msg": "success"
}
```

### FAQ

Q1:Why it only crawls ip and port?

A1:Because the information of the proxy is not completely accurate,it need further verifying.The hproxy will verify whether the proxy is valid and its other information before returning the proxy.

Q2:How to expand data storage mode?

A2:Refer to [BaseDatabase](https://github.com/howie6879/hproxy/blob/master/hproxy/database/base_database.py) which defines some necessary functions required in subclass

Q3:How to expand proxy spider?

A3:Same as above,refer to the spider coding standard in the [spider](https://github.com/howie6879/hproxy/tree/master/hproxy/spider) directory or code in a specific spider script directly. 

### License

hproxy is offered under the MIT license.

### Reference

Thanks for the following items:

- [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)
- [proxy_pool](https://github.com/jhao104/proxy_pool)

Thanks for the following agency website.If you have high-quality agency website,please click here [#3](https://github.com/howie6879/hproxy/issues/3) to submit ^_^.
