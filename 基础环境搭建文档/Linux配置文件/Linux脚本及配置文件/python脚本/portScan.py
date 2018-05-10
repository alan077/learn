import os
import requests,json

def send_weixin(msg):
    corpid="*****************"
    corpsecret="********************************"
    payload={"corpid":corpid,"corpsecret":corpsecret}
    url="https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    message={"touser":"@all",
         "msgtype":"text",
         "agentid":1000003,
         "text":{"content":"检测到非法端口"+str(msg)},
         "safe":0
        }

    re=requests.get(url,params=payload)
    access_token=json.loads(requests.get(url,params=payload).text)
    print(access_token["access_token"])
    access_token={"access_token":access_token["access_token"]}
    send_msg_url="https://qyapi.weixin.qq.com/cgi-bin/message/send"
    #print(message)
    send_msg=requests.post(send_msg_url,params=access_token,data=json.dumps(message).encode('utf-8'))
    #print(send_msg.text)
    #print(send_msg.url)


if __name__=="__main__":

    ip = ["*****", "**************"]
    permit_port=["80","53","443",'']
    warning_port={}
    warning_msg={}
    for node_ip in ip:
        scan = os.popen(
            "nmap -Pn " + node_ip + '''| awk '{line[NR]=$0} END {for(i=6 ;i<=NR-2;i++) print line[i]}' | awk '{if($2=="open") print$1}'| grep -o -E '^.*[0-9]' ''').read()

        a=[]
        for port in scan.split("\n"):
            if port not in permit_port:
                a.append(port)
            warning_port[node_ip]=a

    #非法端口加入到威信消息中
    for key in warning_port.keys():
        if len(warning_port[key])!=0:
            warning_msg[key] = warning_port[key]

    #判断warning_msg是否为空
    if len(warning_msg)!=0:
        send_weixin(warning_msg)
