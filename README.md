## hproxy - 异步IP代理池

本项目利用第三方IP代理提供站定时抓取有效IP，并免费提供网页源数据抓取方案

``` txt

██╗  ██╗██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
██║  ██║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
███████║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝
██╔══██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝
██║  ██║██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║
╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝
```

### 安装

本项目基于Python3.6+，利用Sanic构建异步HTTP服务，利用`aiohttp`进行代理数据异步抓取

``` shell

git clone https://github.com/howie6879/hproxy.git
cd hproxy
pip install pipenv

# 这里需要注意，虚拟环境请使用Python3.6+
pipenv install

# 安装依赖库之后
cd hproxy
python app.py
```

hproxy默认使用Redis进行数据存储服务，所以使用的前提是安装好Redis，具体配置在`config`下：

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

如果想使用机器本身的`Memory`，直接在`config`里将`DB_TYPE = 'redis'`更改为`DB_TYPE = 'memory'`

这里需要注意的是服务停止了数据也随之丢失

如果想使用其他方式进行数据存储，只需根据[BaseDatabase](https://github.com/howie6879/hproxy/blob/master/hproxy/database/base_database.py)的编码规范进行扩展即可

### 特性

- [x] 多种方式进行数据存储，易扩展
    - [DatabaseSetting](https://github.com/howie6879/hproxy/blob/master/hproxy/database/db_setting.py)
    - [Memory](https://github.com/howie6879/hproxy/blob/master/hproxy/database/backends/memory_database.py)
    - [Redis](https://github.com/howie6879/hproxy/blob/master/hproxy/database/backends/redis_database.py)

- [x] 自定义爬虫基础部件，上手简单，统一代码风格：
    - [Field](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base/field.py)
    - [Item](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base/item.py)

- [ ] 提供API获取代理，启动后访问 `127.0.0.1:8001/api`
    - 'delete/:proxy': 'Delete a proxy'
    - 'get': 'Get an usable proxy'
    - 'list': 'List all proxies'

- [ ] 定时抓取、更新

- [ ] 利用代理免费提供网页源码抓取服务 启动后访问 `127.0.0.1:8001/`

- [ ] 抓取监控

### License

hproxy is offered under the MIT 2 license.