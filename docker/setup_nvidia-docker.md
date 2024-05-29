# Setup Nvidia-docker
- update & upgrade
```
sudo apt update && upgrade
```
- install driver

```bash
# install
apt search nvidia-driver
sudo apt install nvidia-driver-<VERSION>

# test
nvidia-smi

## may be reboot
```
- install cuda
    - go to <a href="https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu"> Nvidia developer </a> to download

    - download   

```bash
wget https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux.run
```

* * install

```bash
sudo sh cuda_11.4.1_470.57.02_linux.run
```

``` edit in .bashrc or zshrc```    
```bash
echo "
export PATH=/usr/local/cuda-11.4/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}" >> ~/.bashrc
```

## install docker
- install package

```bash
sudo apt-get update && sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
- install docker
```bash
sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
## post install
```bash
sudo groupadd docker && sudo usermod -aG docker $USER
```

- test
```bash
docker run hello-world
```

# install nvidia-docker
- set
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```
- install
```bash
sudo apt-get update && sudo apt-get install -y nvidia-docker2
```

- restart
```bash
sudo systemctl restart docker
```
- test
```bash
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```