## CentOS7 + docker 部署 hproxy 服务

### 安装 redis

安装 gcc 和 make 编译工具
````shell
yum install -y gcc make
# 若系统安装，跳过此步骤
````

下载 redis 源码包
````shell
curl http://download.redis.io/releases/redis-4.0.9.tar.gz -o redis-4.0.9.tar.gz
````

解压缩
````shell
tar -xzvf redis-4.0.9.tar.gz
````

编译安装 redis
````shell
cd redis-4.0.9
make
make test
make install
````

