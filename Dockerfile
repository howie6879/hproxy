FROM python:3.6
RUN apt update -y && apt-get install -y net-tools
ENV APP_ROOT /data/code
WORKDIR ${APP_ROOT}/
COPY Pipfile ${APP_ROOT}/
COPY Pipfile.lock ${APP_ROOT}/
RUN pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ pipenv
RUN pipenv install
ENV TIME_ZONE=Asia/Shanghai
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
COPY . ${APP_ROOT}
RUN find . -name "*.pyc" -delete
CMD ["pipenv","run","python","hproxy/run.py"]
