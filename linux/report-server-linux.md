# Report command for linux server

### report
- cpu
- memory (ram)
- disk size
- os

### command
```bash
echo "========== CPU ==========" > report.txt && \
lscpu |& head -5 >> report.txt && \ 
echo "========== MEMORY ==========" >> report.txt && \
free -h >> report.txt && \
echo "========== DISK ==========" >> report.txt && \
df -h |& head -5 >> report.txt && \
echo "========== OS ==========" >> report.txt && \
lsb_release -a  >> report.txt && \
cat report.txt
```

### example output
```
========== CPU ==========
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
========== MEMORY ==========
              total        used        free      shared  buff/cache   available
Mem:            15G        3.0G        462M         19M         12G         12G
Swap:            0B          0B          0B
========== DISK ==========
Filesystem      Size  Used Avail Use% Mounted on
udev            7.8G     0  7.8G   0% /dev
tmpfs           1.6G  4.6M  1.6G   1% /run
/dev/sda1       124G   49G   76G  39% /
tmpfs           7.9G     0  7.9G   0% /dev/shm
========== OS ==========
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.6 LTS
Release:        18.04
Codename:       bionic
```