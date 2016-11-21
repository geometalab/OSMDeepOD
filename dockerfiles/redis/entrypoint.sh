#!/bin/bash

redis-server /etc/redis/my_redis.conf
/usr/bin/supervisord

exec "$@"
