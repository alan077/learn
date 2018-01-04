#!/bin/bash
##############################################
#
#
#Filename: login_motd.sh
#
#Description: Print login motd, turn on/off modify in /etc/profile
#	      Usage: 1. disabled /etc/ssh/sshd_config " PrintMotd no "
#		     2. add " bash /usr/profile " function likeness file
##############################################

#variable list
add_name_ip=`ip a s | egrep "inet\b" |egrep -v "host lo" |awk '{print $NF"\t: "$2}'`
kernel_i=`uname -s -r -i`
cpu_i=`grep "model name" /proc/cpuinfo |cut -f2 -d: |uniq -c |sed -r 's/^[[:space:]]+//'`
mem_i=`free -m |grep Mem |awk '{print $3"/"$2" MB"}'`
uptime_i=`uptime |cut -d, -f1 |sed -r 's/^[[:space:]]+//'`
session_i=`who |sed -r 's/\((.*)\)/\1/' |awk '{print "LoginUser: "$1,"\tTime: "$4," IP: "$5}'`
listenP_i=`ss -4antl |egrep -o ":[0-9]+" |sort -n |awk -F: '{printf $2" "}'`

#function list
print_ip_l() {
echo "$add_name_ip" |while read ip_list; do
    echo "+  Address  = $ip_list"
done
}

print_session_l() {
echo "$session_i" |while read session_l; do
    echo "+  Sessions = $session_l"
done
}

#print logo
echo ""
echo -e "\033[33m　　　　　　　＃＃　　　　　  ＃"
echo "　　＃＃　　　＃＃　　　　　＃＃"
echo "　＃＃＃　　　　＃　　　　　　＃　　　　　　　　            ＃＃＃"
echo "　　  ＃　　　　＃　　　　　　＃　＃＃＃　　     　＃＃　 　＃＃＃　　  ＃＃＃＃＃＃　　　＃＃"
echo "　  　＃　　　　＃　＃＃＃　　＃＃＃＃＃　　    ＃＃＃＃　　＃＃    　＃＃＃＃＃＃＃　＃＃＃＃＃＃　＃＃　　＃＃"
echo "    　＃　　　　＃＃＃＃　　　＃＃　＃＃  　   ＃＃　 ＃　  ＃＃　　  ＃＃　＃＃　　　＃＃　　＃＃　　＃　　　＃"
echo "　  　＃　　　　＃＃＃　　　　＃　　　＃　　    ＃＃＃＃　　  ＃　　  ＃＃＃＃＃　　　＃　　　＃＃　　＃　　　＃"
echo "　  　＃　　　　＃＃＃＃　　　＃　　　＃　　  ＃＃＃　＃　　　＃　　  ＃＃　　　　　　＃　　　＃＃　　＃　　　＃"
echo "　  　＃　　　　＃　＃＃　　　＃　　　＃　　  ＃＃　＃＃　　  ＃　　  ＃＃＃＃＃＃　　＃＃　　＃＃　　＃＃　＃＃"
echo "　＃＃＃＃＃　　＃＃＃＃＃　　＃＃＃　＃＃＃  ＃＃＃＃＃＃　＃＃＃＃  ＃＃　　＃＃　　＃＃＃＃＃＃　　＃＃＃＃＃＃"
echo "　　　　　                                      　＃　　　　　　　　　＃＃    ＃＃　　    ＃＃"
echo -e "                                                                      ＃＃＃＃＃＃\033[0m"
echo ""


#print data
echo -e "\033[32m++++++++++++++++++++++ System Data Info ++++++++++++++++++++++\033[0m"
echo "+  Hostname = $HOSTNAME"
print_ip_l
echo "+  Kernel   = $kernel_i"
echo "+  CPU      = $cpu_i"
echo "+  MemAvail = $mem_i"
echo "+  Uptime   = $uptime_i"
echo "+  OpenPort = $listenP_i"
echo -e "\033[32m++++++++++++++++++++++ User Data Info ++++++++++++++++++++++\033[0m"
echo "+  LoginUser= "`whoami`
print_session_l
echo -e "\033[32m++++++++++++++++++++++++ Help Info +++++++++++++++++++++++++\033[0m"
echo "+  Script   = $0"
echo "+  "
echo -e "+  \033[32mWelcome login 1khaigou $HOSTNAME Server ,\033[0m \033[31mPlease prudent operation!!!\033[0m"
echo ""
#end
