#!/bin/bash

redis-server /etc/redis/my_redis.conf
rq-dashboard -P $REDIS_PORT -p $DASHBOARD_PORT --redis-password=crosswalks &
/opt/webdis/webdis

exec "$@"