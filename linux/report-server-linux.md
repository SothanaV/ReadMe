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

# Benchmark
1. install
```
sudo apt-get install stress-ng -y
```

2. run benchmark
```
stress-ng --cpu "$(nproc)" --timeout 30s --metrics
```

output like this
```
stress-ng: info:  [1568506] setting to a 30 secs run per stressor
stress-ng: info:  [1568506] dispatching hogs: 16 cpu
stress-ng: warn:  [1568506] WARNING! using HPET clocksource (refer to /sys/devices/system/clocksource/clocksource0), this may impact benchmarking performance
stress-ng: metrc: [1568506] stressor       bogo ops real time  usr time  sys time   bogo ops/s     bogo ops/s CPU used per       RSS Max
stress-ng: metrc: [1568506]                           (secs)    (secs)    (secs)   (real time) (usr+sys time) instance (%)          (KB)
stress-ng: metrc: [1568506] cpu              534809     30.00    448.82      0.57     17825.52        1190.09        93.61          5616
stress-ng: info:  [1568506] skipped: 0
stress-ng: info:  [1568506] passed: 16: cpu (16)
stress-ng: info:  [1568506] failed: 0
stress-ng: info:  [1568506] metrics untrustworthy: 0
stress-ng: info:  [1568506] successful run completed in 30.01 secs
```