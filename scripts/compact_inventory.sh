#!/bin/bash
# COMPACT INVENTORY - Fits on ONE screenshot
# Output is CSV-ready for easy transcription
H=$(hostname);IP=$(hostname -I 2>/dev/null|awk '{print $1}');MAC=$(ip link show 2>/dev/null|grep -m1 "link/ether"|awk '{print $2}')
CPU=$(grep -m1 "model name" /proc/cpuinfo|cut -d: -f2|xargs);RAM=$(free -h|awk '/Mem:/{print $2}');DISK=$(df -h /|awk 'NR==2{print $2}')
OS=$(cat /etc/os-release 2>/dev/null|grep "^PRETTY"|cut -d= -f2|tr -d '"');KERN=$(uname -r)
echo "=== $H INVENTORY ==="
echo "HOST,$H"
echo "IP,$IP"
echo "MAC,$MAC"
echo "CPU,$CPU"
echo "RAM,$RAM"
echo "DISK,$DISK"
echo "OS,$OS"
echo "KERNEL,$KERN"
echo "--- SOFTWARE ---"
echo "OpenSSH,$(ssh -V 2>&1|awk '{print $1}')"
echo "OpenSSL,$(openssl version 2>/dev/null|awk '{print $2}')"
echo "Bash,$(bash --version|head -1|grep -oP '\d+\.\d+\.\d+')"
echo "Python,$(python3 --version 2>/dev/null|awk '{print $2}')"
echo "Perl,$(perl -v 2>/dev/null|grep -oP 'v\d+\.\d+\.\d+'|head -1)"
echo "Apache,$(apache2 -v 2>/dev/null|head -1|grep -oP '\d+\.\d+\.\d+'||httpd -v 2>/dev/null|head -1|grep -oP '\d+\.\d+\.\d+'||echo N/A)"
echo "Nginx,$(nginx -v 2>&1|grep -oP '\d+\.\d+\.\d+'||echo N/A)"
echo "MySQL,$(mysql --version 2>/dev/null|grep -oP '\d+\.\d+\.\d+'||echo N/A)"
echo "PHP,$(php -v 2>/dev/null|head -1|grep -oP '\d+\.\d+\.\d+'||echo N/A)"
echo "sudo,$(sudo --version 2>/dev/null|head -1|grep -oP '\d+\.\d+\.\d+')"
echo "--- DRIVERS ---"
lsmod|awk 'NR>1&&NR<12{print "DRV,"$1}'
echo "=== END ==="
