# data center
ref : https://developer.nvidia.com/dcgm

- add repo
```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
```

- install
```
sudo apt-get update \
&& sudo apt-get install -y datacenter-gpu-manager
```

- run
```
sudo dcgmi diag -r 1
sudo dcgmi diag -r 2
sudo dcgmi diag -r 3
sudo dcgmi diag -r 4
```