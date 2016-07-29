#!/bin/bash

redis-server --port $REDIS_PORT --daemonize yes
echo "CONFIG SET requirepass 'crosswalks'" | redis-cli -p $REDIS_PORT
rq-dashboard -P $REDIS_PORT -p $DASHBOARD_PORT --redis-password=crosswalks

exec "$@"