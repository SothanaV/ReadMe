# NVIDIA Data Center GPU Manager (DCGM)

DCGM (Data Center GPU Manager) is a suite of tools for managing and monitoring NVIDIA GPUs in data center environments.

Reference: [https://developer.nvidia.com/dcgm](https://developer.nvidia.com/dcgm)

## Install DCGM

### Add the CUDA Repository

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
```

### Install the Package

```bash
sudo apt-get update && sudo apt-get install -y datacenter-gpu-manager
```

## Run Diagnostics

DCGM provides four diagnostic levels. Higher levels run more thorough tests but take longer:

```bash
sudo dcgmi diag -r 1   # Quick health check (~1 minute)
sudo dcgmi diag -r 2   # Medium diagnostics (~2 minutes)
sudo dcgmi diag -r 3   # Long diagnostics (~5 minutes)
sudo dcgmi diag -r 4   # Extended diagnostics (stress test)
```

## Run the DCGM Exporter for Grafana

The DCGM Exporter exposes GPU metrics on a Prometheus-compatible HTTP endpoint, which can then be scraped and visualised in Grafana.

```bash
docker run -d \
  --gpus all \
  --cap-add SYS_ADMIN \
  --rm \
  -p 9400:9400 \
  -e DCGM_EXPORTER_INTERVAL=100 \
  nvcr.io/nvidia/k8s/dcgm-exporter:4.2.0-4.1.0-ubuntu22.04
```

- `DCGM_EXPORTER_INTERVAL` — metric collection interval in milliseconds (100 ms = 10 samples per second).

Verify metrics are being exposed:

```bash
curl http://localhost:9400/metrics
```

## Run the GPU Benchmark Script

The benchmark script collects live GPU metrics during a load test and produces a summary report.

### Requirements

```bash
pip install pandas matplotlib seaborn
```

### Run

```bash
python benchmark.py
```

### Example Output

```text
Starting GPU metrics collection...
Starting load test with 50 concurrent requests...
Stopping GPU metrics collection...

### Load Test Results ###
#### Input Parameters
- **Input query tokens per request**: 1317.76
- **Number of requests per second**: 0.24
#### Process
- **LLM processing time**: 103.34 seconds
- **Average GPU core utilization**: 78.79%
- **Average GPU memory utilization**: 81.29%
#### Output Parameters
- **Output tokens per request**: 791.96

Total duration: 204.64 seconds
Total requests: 50
```
