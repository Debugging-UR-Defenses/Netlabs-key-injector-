#!/bin/bash
# Driver Inventory Script for NDG Security+ Lab
# Run this on each Linux host (not Kali)
# Lists 10+ drivers/kernel modules

echo "=========================================="
echo "DRIVER INVENTORY - $(hostname)"
echo "Date: $(date)"
echo "=========================================="

echo ""
echo "--- LOADED KERNEL MODULES (Top 15) ---"
lsmod | head -16
echo ""

echo "--- NETWORK DRIVERS ---"
lspci -k 2>/dev/null | grep -A 3 -i network
echo ""

echo "--- STORAGE DRIVERS ---"
lspci -k 2>/dev/null | grep -A 3 -i storage
echo ""

echo "--- VIDEO/GRAPHICS DRIVERS ---"
lspci -k 2>/dev/null | grep -A 3 -i vga
echo ""

echo "--- USB DRIVERS ---"
lspci -k 2>/dev/null | grep -A 3 -i usb | head -10
echo ""

echo "--- DETAILED MODULE INFO (First 10 modules) ---"
for mod in $(lsmod | awk 'NR>1 {print $1}' | head -10); do
    echo "Module: $mod"
    modinfo $mod 2>/dev/null | grep -E "^version:|^description:" || echo "  No version info"
    echo ""
done

echo "--- KERNEL VERSION ---"
uname -r
echo ""

echo "--- DRIVER FILES IN /lib/modules ---"
ls /lib/modules/$(uname -r)/kernel/drivers/ 2>/dev/null | head -10
echo ""

echo "=========================================="
echo "END DRIVER INVENTORY"
echo "=========================================="
