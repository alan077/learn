#!/bin/bash
#Linxu安装使用最小化安装模式，安装完成后安装基础软件，更好Centos源
rpm -aq |grep wget
if [ $? -ne 0 ];then
    yum -y install vim wget ntp gcc gcc-c++
else
    wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
fi
A="更新Centos源文件"
if [ $? -eq 0 ];then
    echo "$A成功"
    yum makecache
else
    echo "$A失败"
    exit
fi
A="关闭防火墙"
chkconfig iptables off && /etc/init.d/iptables stop
if [ $? -eq 0 ];then
    echo "$A成功"
else
    echo "$A失败"
    exit
fi
#关闭selinux
A="关闭selinux"
sed -i 's/SELINUX=enforcing/SELINUX=disablesd/g' /etc/selinux/config
if [ $? -eq 0 ];then
    echo "$A成功"
else
    echo "$A失败"
    exit
fi
#关闭control-alt-delete重启
A="关闭control-alt-delete重启"
sed -i 's/exec/#exec/g' /etc/init/control-alt-delete.conf
if [ $? -eq 0 ];then
    echo "$A成功"
else
    echo "$A失败"
    exit
fi
#修改ssh配置文件
A="优化ssh配置文件"
sed -i 's/#MaxAuthTries/MaxAuthTries/g' /etc/ssh/sshd_config
sed -i 's/#UseDNS/UseDNS/g' /etc/ssh/sshd_config
sed -i 's/#ClientAliveInterval/ClientAliveInterval/g' /etc/ssh/sshd_config
sed -i 's/#ClientAliveCountMax/ClientAliveCountMax/g' /etc/ssh/sshd_config
if [ $? -eq 0 ];then
    echo "$A成功"
else
    echo "$A失败"
    exit
fi
#调整文件描述符大小
A="调整文件描述符大小"
echo -e 'root soft nofile 65535' >> /etc/security/limits.conf
echo -e 'root hard nofile 65535' >> /etc/security/limits.conf
echo -e '* soft nofile 65535' >> /etc/security/limits.conf
echo -e '* hard nofile 65535' >> /etc/security/limits.conf
if [ $? -eq 0 ];then
    echo "$A成功"
else
    echo "$A失败"
    exit
fi
#设置时间同步
A="设置时间同步"
ntpdate cn.pool.ntp.org && hwclock -w && echo -e '* * * * * /usr/sbin/ntpdate cn.pool.ntp.org && hwclock -w &> /dev/null' >>/var/spool/cron/root
if [ $? -eq 0 ];then
    echo "$A成功"
else
    echo "$A失败"
    exit
fi
#优化内核参数
A="优化内核参数"
echo -e "# see details in https://help.aliyun.com/knowledge_detail/39428.html" >> /etc/sysctl.conf
echo -e "net.ipv4.conf.all.rp_filter=0" >> /etc/sysctl.conf
echo -e "net.ipv4.conf.default.rp_filter=0" >> /etc/sysctl.conf
echo -e "net.ipv4.conf.default.arp_announce = 2" >> /etc/sysctl.conf
echo -e "net.ipv4.conf.lo.arp_announce=2" >> /etc/sysctl.conf
echo -e "net.ipv4.conf.all.arp_announce=2" >> /etc/sysctl.conf
echo -e "# see details in https://help.aliyun.com/knowledge_detail/41334.html" >> /etc/sysctl.conf
echo -e "net.ipv4.tcp_max_tw_buckets = 5000" >> /etc/sysctl.conf
echo -e "net.ipv4.tcp_syncookies = 1" >> /etc/sysctl.conf
echo -e "net.ipv4.tcp_max_syn_backlog = 1024" >> /etc/sysctl.conf
echo -e "net.ipv4.tcp_synack_retries = 2" >> /etc/sysctl.conf
echo -e "net.ipv4.tcp_tw_reuse = 1" >> /etc/sysctl.conf
echo -e "net.ipv4.tcp_tw_recycle = 1" >> /etc/sysctl.conf
echo -e "net.ipv4.tcp_fin_timeout = 30" >> /etc/sysctl.conf
#sysctl -p
if [ $? -eq 0 ];then
    echo "$A成功"
    reboot
else
    echo "$A失败"
    exit
fi