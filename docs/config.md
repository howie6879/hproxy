# hproxy 服务配置说明

为了方便更改hproxy项目的配置，使用者可根据系统环境变量来对项目一些参数配置进行更改，目前hproxy的基本配置如下：

``` python
import os


class Config():
    """
    Basic config for hproxy
    """

    # Application config
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DB_TYPE = os.getenv('DB_TYPE', "redis")
    HOST = ['127.0.0.1:8001', '0.0.0.0:8001']
    START_SPIDER = str(os.getenv('START_SPIDER', '1'))
    TIMEZONE = 'Asia/Shanghai'
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    VAL_HOST = str(os.getenv('VAL_HOST', '0'))

    # scheduled task
    SCHEDULED_DICT = {
        'ver_interval': int(os.getenv('VER_INTERVAL', 10)),
        'spider_interval': int(os.getenv('SPIDER_INTERVAL', 60)),
    }

    # URL config
    TEST_URL = {
        'http': 'http://httpbin.org/get?show_env=1',
        'https': 'https://httpbin.org/get?show_env=1',
        'timeout': 5
    }
```

配置参数说明：

| 参数            | 说明                                     |
| --------------- | ---------------------------------------- |
| DB_TYPE         | redis或者memory两种类型，建议redis       |
| START_SPIDER    | 1或0，是否在项目启动时候马上爬取代理网站 |
| TIMEZONE        | 地域                                     |
| USER_AGENT      | 默认UA                                   |
| VAL_HOST        | 0或1，是否验证请求host，默认不验证       |
| VER_INTERVAL    | 定时验证代理数据时间                     |
| SPIDER_INTERVAL | 定时爬取代理数据时间                     |