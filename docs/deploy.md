# docker 部署 hproxy 服务

## 安装 redis

安装 gcc 和 make 编译工具
````shell
# 若系统安装，跳过此步骤

# CentOS
yum install -y gcc make wget

# Ubuntu
apt install -y gcc make wget
````

下载 redis 源码包
````shell
wget http://download.redis.io/redis-stable.tar.gz
````

解压缩
````shell
tar -xzvf redis-stable.tar.gz
````

编译安装 redis
````shell
cd redis-stable
# 编译
make
# 校验
make test
# 校验成功，进行安装
make install
````

## 配置 redis
创建配置文件目录，数据库 dump file 目录，进程 pid 目录，日志 log 目录
````shell
# 配置文件目录放在 /etc/ 下
mkdir /etc/redis
# dump file 目录、pid 目录、log 目录放在 /var/ 下
mkdir /var/redis
cd /var/redis
mkdir data run log
````

返回源码包，将源码包下的 redis.conf 复制到配置文件目录 /etc/redis
````shell
cp redis.conf /etc/redis
````

### 修改 redis 配置参数
````shell
emacs /etc/redis/redis.conf
````

使 redis 能在后台运行
````shell
daemonize yes
````

修改pid目录为新建目录
````shell
pidfile /var/redis/run/redis.pid
````

修改dump目录为新建目录
````shell
dir /var/redis/data
````

修改log存储目录为新建目录
````shell
logfile /var/redis/log/redis.log
````

启动 redis 服务
````shell
redis-server /etc/redis/redis.conf
````

启动 redis 客户端
````shell
redis-cli
# ctrl + d 退出客户端
````

停止 redis 服务
````shell
ps -ax|grep redis|awk '{print $1}'|xargs kill -9
````
至此，redis 的安装和基本配置就完成了

## 安装 docker
````shell
# 官方下载方式
curl -sSL https://get.docker.com/ | sh

# 阿里云的安装脚本，可以提高下载速度
curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh
````

将用户加入 docker 用户组
````shell
sudo usermod -aG docker $USER
````

启动 docker
````shell
systemctl start docker
````

查看 docker 信息
````shell
docker info
````

查看 docker 镜像
````shell
docker images
````

查看 docker 运行中的镜像
````shell
docker ps
````

终止 docker 运行中的镜像
````shell
docker ps|grep 镜像名称|awk '{print $1}'|xargs docker kill
````

## 创建 hproy 镜像
clone hproxy
````shell
git clone git clone https://github.com/howie6879/hproxy.git
````

生成 hproxy 镜像
````shell
# 进入 hproxy 项目目录
cd hproxy
# 执行创建命令，注意最后的参数，指的是 Dockerfile 所在路径为当前目录
docker image built -t hproxy .
# 查看创建的镜像
docker images
````

设置 redis
````shell
# 修改 hproxy 项目目录下的 hproxy.env 文件，根据自身环境，修改其中的 redis 设置
emacs hproxy.env
````

运行 hproxy
````shell
# 加载 hproxy.env，并将 docker 的8001端口映射到主机的8001端口
docker run --env-file ./hproxy.env -d -p 8001:8001 hproxy
````