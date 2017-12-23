#!/bin/shell
#Redis状态监测
i=1
while [ $i -le 3 ];do
    Status=`/usr/local/bin/redis-cli -h 127.0.0.1 -p 6379 -a lcb@redis.com ping |grep -c PONG`
    if [ $Status -ne 1 ];then
        ((i=$i+1))
        /etc/init.d/redis restart
        sleep 5
    else
        exit 0
    fi
done
