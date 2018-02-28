#!/bin/bash
#########################################################################
# File Name: wechat.sh
# Author: shaonbean
# Email: shaonbean@qq.com
# Created Time: Sun 24 Jul 2016 05:48:14 AM CST
#########################################################################
# Functions: send messages to wechat app
# set variables
CropID='wx264347793b3b9207'
Secret='yckV8gOAcFytc32ivaxBuhcC4xJqtsIvc49Z8OUoH9YxrfV29AxI51j86ZwMETT_'
GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CropID&corpsecret=$Secret"
#get acccess_token
Gtoken=$(/usr/bin/curl -s -G $GURL | awk -F\" '{print $4}')
PURL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$Gtoken"
#
function body() {
local int AppID=1                         #企业号中的应用id
local UserID="$1"                         #部门成员id，zabbix中定义的微信接收者
local PartyID=1                           #部门id，定义了范围，组内成员都可接收到消息
local Msg=$(echo "$@" | cut -d" " -f3-)   #过滤出zabbix传递的第三个参数
printf '{\n'
printf '\t"touser": "'"$UserID"\"",\n"
printf '\t"toparty": "'"$PartyID"\"",\n"
printf '\t"msgtype": "text",\n'
printf '\t"agentid": "'" $AppID "\"",\n"
printf '\t"text": {\n'
printf '\t\t"content": "'"$Msg"\""\n"
printf '\t},\n'
printf '\t"safe":"0"\n'
printf '}\n'
}
/usr/bin/curl --data-ascii "$(body $1 $2 $3)" $PURL
#http://qydev.weixin.qq.com/wiki/index.php?title=消息类型及数据格式
#测试：




bash wechat.sh  微信号 test hello.world!
{"errcode":0,"errmsg":"ok","invaliduser":"all user invalid"}