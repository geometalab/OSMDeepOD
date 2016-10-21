FROM django:latest

MAINTAINER Samuel Kurath <skurath@hsr.ch>

ENV REDIS_PORT 40001
ENV DASHBOARD_PORT 40002

EXPOSE $REDIS_PORT $DASHBOARD_PORT

COPY entrypoint.sh /
COPY my_redis.conf /etc/redis/
COPY my_webdis.json /opt/
COPY server.c /opt/
COPY conf.c /opt/
COPY conf.h /opt/

ENTRYPOINT ["./entrypoint.sh"]

RUN apt-get update -y \
&& apt-get upgrade -y \
&& apt-get install -y redis-server libevent-dev git vim build-essential\
&& pip install rq-dashboard \
&& mkdir /redis/ \
&& cd /opt/ \
&& git clone https://github.com/nicolasff/webdis.git \
&& mv my_webdis.json /opt/webdis/webdis.json \
&& mv server.c /opt/webdis/server.c \
&& mv conf.c /opt/webdis/conf.c \
&& mv conf.h /opt/webdis/conf.h \
&& cd webdis \
&& make clean all \
&& chmod +x /entrypoint.sh \




