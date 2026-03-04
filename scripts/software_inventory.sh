#!/bin/bash
# Software Inventory Script for NDG Security+ Lab
# Run this on each Linux host (not Kali)
# Lists 10+ applications with versions

echo "=========================================="
echo "SOFTWARE INVENTORY - $(hostname)"
echo "Date: $(date)"
echo "=========================================="

echo ""
echo "--- OS VERSION ---"
cat /etc/os-release 2>/dev/null || cat /etc/*release 2>/dev/null
echo ""

echo "--- KERNEL VERSION ---"
uname -r
echo ""

echo "--- TOP 10 INSTALLED PACKAGES (Debian/Ubuntu) ---"
dpkg -l 2>/dev/null | grep "^ii" | head -15 | awk '{print $2, $3}'
echo ""

echo "--- TOP 10 INSTALLED PACKAGES (RHEL/CentOS) ---"
rpm -qa --queryformat '%{NAME} %{VERSION}-%{RELEASE}\n' 2>/dev/null | head -15
echo ""

echo "--- KEY APPLICATIONS WITH VERSIONS ---"
echo "Apache:" && apache2 -v 2>/dev/null || httpd -v 2>/dev/null || echo "Not installed"
echo ""
echo "Nginx:" && nginx -v 2>&1 || echo "Not installed"
echo ""
echo "OpenSSH:" && ssh -V 2>&1
echo ""
echo "OpenSSL:" && openssl version 2>/dev/null || echo "Not installed"
echo ""
echo "Python:" && python3 --version 2>/dev/null || python --version 2>/dev/null || echo "Not installed"
echo ""
echo "Perl:" && perl -v 2>/dev/null | grep version | head -1 || echo "Not installed"
echo ""
echo "Bash:" && bash --version | head -1
echo ""
echo "MySQL/MariaDB:" && mysql --version 2>/dev/null || echo "Not installed"
echo ""
echo "PostgreSQL:" && psql --version 2>/dev/null || echo "Not installed"
echo ""
echo "PHP:" && php -v 2>/dev/null | head -1 || echo "Not installed"
echo ""

echo "--- RUNNING SERVICES ---"
systemctl list-units --type=service --state=running 2>/dev/null | head -15 || service --status-all 2>/dev/null | grep "+" | head -15
echo ""

echo "--- LISTENING PORTS ---"
ss -tuln 2>/dev/null | head -15 || netstat -tuln 2>/dev/null | head -15
echo ""

echo "=========================================="
echo "END SOFTWARE INVENTORY"
echo "=========================================="
