# I/O Test
- install fio
```
apt update 
apt install -y fio
```

- create file
```
dd if=/dev/zero of=/app/backend/data/testfile bs=1M count=1000 oflag=dsync
```
- test
```
fio --name=hpe-csi-test --size=1G --filename=/app/backend/data/testfile --bs=4k --rw=randrw --ioengine=libaio --direct=1 --numjobs=4 --time_based --runtime=60 --group_reporting
```


## example report
```
hpe-test-macbook-air: (g=0): rw=randrw, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=psync, iodepth=1
...
fio-3.39
Starting 4 processes
hpe-test-macbook-air: Laying out IO file (1 file / 1024MiB)
Jobs: 4 (f=4): [m(4)][100.0%][r=53.1MiB/s,w=52.7MiB/s][r=13.6k,w=13.5k IOPS][eta 00m:00s]
hpe-test-macbook-air: (groupid=0, jobs=4): err= 0: pid=12645: Wed Mar 12 16:42:53 2025
  read: IOPS=12.6k, BW=49.4MiB/s (51.8MB/s)(2962MiB/60001msec)
    clat (nsec): min=0, max=25854k, avg=141256.11, stdev=329012.73
     lat (nsec): min=0, max=25854k, avg=141284.32, stdev=329015.49
    clat percentiles (nsec):
     |  1.00th=[   1004],  5.00th=[  70144], 10.00th=[  73216],
     | 20.00th=[  77312], 30.00th=[  81408], 40.00th=[  84480],
     | 50.00th=[  87552], 60.00th=[  90624], 70.00th=[  95744],
     | 80.00th=[ 102912], 90.00th=[ 127488], 95.00th=[ 175104],
     | 99.00th=[1941504], 99.50th=[2023424], 99.90th=[2736128],
     | 99.95th=[3293184], 99.99th=[7438336]
   bw (  KiB/s): min= 4372, max=69202, per=100.00%, avg=50578.44, stdev=2485.68, samples=476
   iops        : min= 1090, max=17298, avg=12643.24, stdev=621.41, samples=476
  write: IOPS=12.7k, BW=49.5MiB/s (51.9MB/s)(2968MiB/60001msec); 0 zone resets
    clat (nsec): min=1000, max=23966k, avg=174052.84, stdev=322403.59
     lat (nsec): min=1000, max=23966k, avg=174219.15, stdev=322547.00
    clat percentiles (usec):
     |  1.00th=[    6],  5.00th=[   94], 10.00th=[  101], 20.00th=[  106],
     | 30.00th=[  112], 40.00th=[  116], 50.00th=[  120], 60.00th=[  125],
     | 70.00th=[  130], 80.00th=[  141], 90.00th=[  172], 95.00th=[  223],
     | 99.00th=[ 1991], 99.50th=[ 2073], 99.90th=[ 2769], 99.95th=[ 3294],
     | 99.99th=[ 7046]
   bw (  KiB/s): min= 4356, max=70716, per=100.00%, avg=50683.66, stdev=2489.44, samples=476
   iops        : min= 1086, max=17678, avg=12669.53, stdev=622.37, samples=476
  lat (nsec)   : 2=0.01%
  lat (usec)   : 2=0.67%, 4=0.92%, 10=1.23%, 20=0.23%, 50=0.34%
  lat (usec)   : 100=38.42%, 250=54.22%, 500=1.15%, 750=0.20%, 1000=0.12%
  lat (msec)   : 2=1.70%, 4=0.76%, 10=0.03%, 20=0.01%, 50=0.01%
  cpu          : usr=0.40%, sys=6.61%, ctx=1550087, majf=0, minf=32
  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwts: total=758360,759868,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=49.4MiB/s (51.8MB/s), 49.4MiB/s-49.4MiB/s (51.8MB/s-51.8MB/s), io=2962MiB (3106MB), run=60001-60001msec
  WRITE: bw=49.5MiB/s (51.9MB/s), 49.5MiB/s-49.5MiB/s (51.9MB/s-51.9MB/s), io=2968MiB (3112MB), run=60001-60001msec
```