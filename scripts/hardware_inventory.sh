#!/bin/bash
# Hardware Inventory Script for NDG Security+ Lab
# Run this on each Linux host (not Kali)

echo "=========================================="
echo "HARDWARE INVENTORY - $(hostname)"
echo "Date: $(date)"
echo "=========================================="

echo ""
echo "--- SYSTEM INFO ---"
uname -a
echo ""

echo "--- CPU INFO ---"
cat /proc/cpuinfo | grep -E "model name|processor|cpu cores" | head -6
echo ""

echo "--- MEMORY INFO ---"
free -h
echo ""

echo "--- DISK INFO ---"
df -h
echo ""

echo "--- NETWORK INTERFACES ---"
ip addr show 2>/dev/null || ifconfig
echo ""

echo "--- MAC ADDRESSES ---"
ip link show 2>/dev/null | grep -E "link/ether" || ifconfig | grep -i ether
echo ""

echo "--- PCI DEVICES (Hardware) ---"
lspci 2>/dev/null | head -20
echo ""

echo "--- USB DEVICES ---"
lsusb 2>/dev/null
echo ""

echo "--- BLOCK DEVICES ---"
lsblk 2>/dev/null
echo ""

echo "=========================================="
echo "END HARDWARE INVENTORY"
echo "=========================================="
