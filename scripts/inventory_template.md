# NDG Security+ v3 Lab 2 - Inventory Template

## Instructions
1. Use the key injector to run each script on target hosts
2. Take screenshots of the output
3. Paste screenshots into an AI for text extraction
4. Fill in the tables below with extracted data

---

## Hardware Inventory

| Hostname | IP Address | MAC Address | CPU | RAM | Disk | OS |
|----------|------------|-------------|-----|-----|------|----|
| Host1 | | | | | | |
| Host2 | | | | | | |
| Host3 | | | | | | |

---

## Software Inventory (10 Apps per Linux Host)

| Hostname | Software | Installed Version | Current Version | Vulnerable? | CVE/Notes |
|----------|----------|-------------------|-----------------|-------------|-----------|
| | OpenSSH | | | | |
| | OpenSSL | | | | |
| | Apache/Nginx | | | | |
| | Python | | | | |
| | Bash | | | | |
| | MySQL/MariaDB | | | | |
| | PHP | | | | |
| | Perl | | | | |
| | Kernel | | | | |
| | sudo | | | | |

---

## Driver Inventory (10 Drivers)

| Hostname | Driver/Module | Version | Description | Vulnerable? | CVE/Notes |
|----------|---------------|---------|-------------|-------------|-----------|
| | | | | | |
| | | | | | |
| | | | | | |

---

## Vulnerability Research Resources

- **NVD (National Vulnerability Database)**: https://nvd.nist.gov/
- **CVE Details**: https://www.cvedetails.com/
- **Exploit-DB**: https://www.exploit-db.com/
- **MITRE CVE**: https://cve.mitre.org/

### How to Research
1. Search NVD for: `[software name] [version]`
2. Check if installed version < patched version
3. Note CVE IDs and severity scores (CVSS)

---

## Quick Commands to Copy

### Run all inventories and save to file:
```bash
./hardware_inventory.sh > hw_inventory.txt
./software_inventory.sh > sw_inventory.txt
./driver_inventory.sh > drv_inventory.txt
```

### View output in chunks (for screenshots):
```bash
head -30 hw_inventory.txt
tail -30 hw_inventory.txt
sed -n '31,60p' hw_inventory.txt
```
