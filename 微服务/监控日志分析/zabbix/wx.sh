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
local int AppID=1                         #��ҵ���е�Ӧ��id
local UserID="$1"                         #���ų�Աid��zabbix�ж����΢�Ž�����
local PartyID=1                           #����id�������˷�Χ�����ڳ�Ա���ɽ��յ���Ϣ
local Msg=$(echo "$@" | cut -d" " -f3-)   #���˳�zabbix���ݵĵ���������
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
#http://qydev.weixin.qq.com/wiki/index.php?title=��Ϣ���ͼ����ݸ�ʽ
#���ԣ�




bash wechat.sh  ΢�ź� test hello.world!
{"errcode":0,"errmsg":"ok","invaliduser":"all user invalid"}