#!/bin/bash
Date_Status(){
    DATE=`date +%Y%m%d%H%M%S`
}
Send_Mail01(){
    Date_Status
    mailsubject="�ڽ�Դվ�������"
    mailbody="$DATE :�ڽ�Դվ������ϣ�����80�˿�״̬��$Port1 ��ͨ80�˿�״̬��$Port2"
    echo $mailbody | mail -s "$mailsubject" $contact1 $contact2
}



echo "��վ����" | mail -s "��վ����" 370220760@qq.com zabbix@777.com