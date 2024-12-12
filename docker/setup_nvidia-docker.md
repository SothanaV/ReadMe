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

# install docker
- [install docker](./docker-install.md)


# install nvidia-docker
[container-toolkit install-guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- config repo
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
- install
```bash
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
```

- config
```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

- test
```bash
sudo docker run --rm --gpus all nvidia/cuda:12.6.3-base-ubuntu24.04 nvidia-smi
```