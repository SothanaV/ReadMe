# Packages for Work on Ubuntu

A reference list of tools and applications commonly installed on an Ubuntu workstation for development and operations work.

## Communication

### Microsoft Teams

```bash
sudo snap install teams-for-linux
```

## Kubernetes Tools

### Lens (Kubernetes IDE)

```bash
sudo snap install kontena-lens --classic
```

> Note: Lens has been rebranded. The community fork is available at [OpenLens](https://github.com/MuhammedKalkan/OpenLens) if the Snap package is no longer maintained.

## Development Tools

### Visual Studio Code

```bash
sudo snap install code --classic
```

### Docker

```bash
sudo apt update
sudo apt install docker.io -y
sudo usermod -aG docker $USER
```

### kubectl

```bash
sudo snap install kubectl --classic
kubectl version --client
```

### Helm

```bash
sudo snap install helm --classic
```

## Productivity

### Postman

```bash
sudo snap install postman
```

### DBeaver (Database Client)

```bash
sudo snap install dbeaver-ce
```

## System Utilities

### htop

```bash
sudo apt install htop -y
```

### net-tools (ifconfig, netstat)

```bash
sudo apt install net-tools -y
```

### curl and wget

```bash
sudo apt install curl wget -y
```
