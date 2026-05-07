# Nvidia GPU Grafana Dashboard Monitoring

Guide for setting up NVIDIA GPU monitoring using DCGM Exporter, Prometheus, and Grafana.

## Prerequisites

- NVIDIA GPU with supported architecture
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) (nvidia-docker) installed
- Docker or Docker Compose installed
- Prometheus installed and configured
- Grafana installed and configured

## Step 1: Deploy DCGM Exporter

DCGM (Data Center GPU Manager) Exporter collects GPU metrics and exposes them via Prometheus-compatible endpoint.

### Docker Compose Configuration

Reference: [DCGM Exporter Documentation](https://docs.nvidia.com/datacenter/dcgm/latest/gpu-telemetry/dcgm-exporter.html)

```yaml
services:
  nvidia-exporter:
    container_name: nvidia-exporter
    image: nvcr.io/nvidia/k8s/dcgm-exporter:4.5.2-4.8.1-distroless
    restart: always
    ports:
      - "9400:9400"
    runtime: nvidia
    environment:
      - DCGM_EXPORTER_INTERVAL=1000
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              capabilities: [gpu]
```

### Start the Exporter

```bash
docker compose up -d
```

### Verify Metrics Endpoint

```bash
curl http://localhost:9400/metrics
```

## Step 2: Configure Prometheus Scrape Target

Add the DCGM exporter as a scrape target in your Prometheus configuration (`prometheus.yml`):

```yaml
scrape_configs:
  - job_name: "nvidia-gpu"
    scrape_interval: 2s
    static_configs:
      - targets:
          - "<serverIP>:9400"
```

> Replace `<serverIP>` with the actual server or container IP address.

### Restart Prometheus

```bash
# If running as a container
docker restart prometheus

# If using systemd
sudo systemctl restart prometheus
```

### Verify Prometheus Target

Navigate to `http://<prometheus-ip>:9090/targets` and confirm the `nvidia-gpu` job is **UP**.

## Step 3: Import Grafana Dashboard

### Option A: Import from Grafana.com

1. Download the dashboard template ID: **[15117 - NVIDIA DCGM Exporter](https://grafana.com/grafana/dashboards/15117-nvidia-dcgm-exporter/)**
2. In Grafana, go to **Dashboards → Import**
3. Enter `15117` in the "Grafana.com Dashboard" field
4. Click **Load**, select your data source (Prometheus), and click **Import**

### Option B: Manual JSON Import

1. Download the JSON file from the link above
2. In Grafana, go to **Dashboards → Import**
3. Click **Upload JSON file** and select the downloaded file
4. Select your Prometheus data source and click **Import**

## Dashboard Features

The imported dashboard provides:

- GPU utilization and memory usage
- GPU temperature
- GPU power consumption
- GPU clock frequencies
- ECC memory errors
- GPU temperature and throttling info
- NVLink metrics (if supported)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| DCGM exporter fails to start | Ensure NVIDIA Container Toolkit is installed and `nvidia-smi` works on host |
| No metrics in Prometheus | Check firewall allows port `9400`, verify target is UP in Prometheus targets |
| Grafana shows no data | Verify Prometheus data source is correctly configured in Grafana |
| GPU metrics not appearing | Run `nvidia-smi` on the host to verify GPU accessibility |

## References

- [DCGM Exporter Docs](https://docs.nvidia.com/datacenter/dcgm/latest/gpu-telemetry/dcgm-exporter.html)
- [Grafana Dashboard 15117](https://grafana.com/grafana/dashboards/15117-nvidia-dcgm-exporter/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

