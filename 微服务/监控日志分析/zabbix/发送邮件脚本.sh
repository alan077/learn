#!/bin/bash
Date_Status(){
    DATE=`date +%Y%m%d%H%M%S`
}
Send_Mail01(){
    Date_Status
    mailsubject="ÈÚ½ğ±¦Ô´Õ¾ÍøÂç¹ÊÕÏ"
    mailbody="$DATE :ÈÚ½ğ±¦Ô´Õ¾ÍøÂç¹ÊÕÏ£¬µçĞÅ80¶Ë¿Ú×´Ì¬£º$Port1 ÁªÍ¨80¶Ë¿Ú×´Ì¬£º$Port2"
    echo $mailbody | mail -s "$mailsubject" $contact1 $contact2
}



echo "ÍøÕ¾¹ÊÕÏ" | mail -s "ÍøÕ¾¹ÊÕÏ" 370220760@qq.com zabbix@777.com