## hproxy - 异步IP代理池

[![Build Status](https://travis-ci.org/howie6879/hproxy.svg?branch=master)](https://travis-ci.org/howie6879/hproxy)

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

# 启动爬虫 运行 /hproxy/hproxy/spider/spider_console.py
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

这里需要注意的是如果使用`memory`模式，那么服务停止了数据也随之丢失

如果想使用其他方式进行数据存储，只需根据[BaseDatabase](https://github.com/howie6879/hproxy/blob/master/hproxy/database/base_database.py)的编码规范进行扩展即可

### 特性

- [x] 多种方式进行数据存储，易扩展：
    - [DatabaseSetting](https://github.com/howie6879/hproxy/blob/master/hproxy/database/db_setting.py)
    - [Memory](https://github.com/howie6879/hproxy/blob/master/hproxy/database/backends/memory_database.py)
    - [Redis](https://github.com/howie6879/hproxy/blob/master/hproxy/database/backends/redis_database.py)
- [x] 自定义爬虫基础部件，上手简单，统一代码风格：
    - [Field](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base/field.py)
    - [Item](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base/item.py)
- [x] 提供API获取代理，启动后访问 `127.0.0.1:8001/api`
    - 'delete/:proxy': 'Delete a proxy'
    - 'get': 'Get an usable proxy'
    - 'list': 'List all proxies'
- [ ] 定时抓取、更新、自动验证ip的类型：如代理类型、协议、位置
- [ ] 利用代理免费提供网页源码抓取服务 启动后访问 `127.0.0.1:8001/`
- [ ] 抓取监控

### 功能描述

#### 代理获取

本项目的爬虫代码全部集中于目录[spider](https://github.com/howie6879/hproxy/tree/master/hproxy/spider)，在[/spider/proxy_spider/](https://github.com/howie6879/hproxy/tree/master/hproxy/spider/proxy_spider)目录下定义了一系列代理网站的爬虫，所有爬虫基于[/spider/base/proxy_spider.py](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/base/proxy_spider.py)里定义的规范编写，参考这些，就可以很方便的扩展一系列代理爬虫

运行[spider_console.py](https://github.com/howie6879/hproxy/blob/master/hproxy/spider/spider_console.py)文件，即可启动全部爬虫进行代理的获取，无需定义新加的爬虫脚本，只需按照规范命名，即可自动获取爬虫模块然后运行

#### 代理接口

| 接口          | 描述                                                         |
| :------------ | :----------------------------------------------------------- |
| delete/:proxy | 删除一个代理                                                 |
| get           | 参数valid=1，会在返回代理过程中验证一次，确保其有效，否则一直寻找，直到返回 |
| list          | 列出所有代理，没有一个个验证                                 |
| valid/:proxy  | 验证一个代理                                                 |

``` json
// http://127.0.0.1:8001/api/get?valid=1
// 返回成功，开启验证参数valid=1的话speed会有值，并且默认是开启的
{
    status: 1,
    info: {
        proxy: "119.28.112.130:3128",
        details: { }
    },
    msg: "success",
    speed: 0.4441831112
}
// http://127.0.0.1:8001/api/list 列出所有代理，没有一个个验证
{
    status: 1,
    info: [
    "171.39.45.6:8123",
    "183.159.91.75:18118",
    "111.155.116.234:8123"
    ],
    msg: "success"
}
// http://127.0.0.1:8001/api/delete/171.39.45.6:8123
{
    status: 1,
    msg: "success"
}
// http://127.0.0.1:8001/api/valid/183.159.91.75:18118
{
    status: 1,
    msg: "success",
    speed: 0.6555871964
}
```



### 代理网站

目前代理网站如下，有优质代理网站请提交^_^

- [西刺代理](http://www.xicidaili.com/)
- [66免费代理网](http://www.66ip.cn/)

### FAQ

问：为什么只抓取ip以及端口？

答：因为网站上代理的信息不一定准确，所以需要进一步验证，本项目会在返回代理的时候做进行验证，验证是否可用以及验证代理具体信息

问：如何扩展数据存储方式？

答：[BaseDatabase](https://github.com/howie6879/hproxy/blob/master/hproxy/database/base_database.py)里面定义了一些子类必须要有的方法，按照这个格式写就不会有问题

问：如何扩展代理爬虫？

答：同样，在[spider](https://github.com/howie6879/hproxy/tree/master/hproxy/spider)目录下找到爬虫编写规范，或者直接看某一个代理爬虫脚本的编写模式。


### License

hproxy is offered under the MIT license.