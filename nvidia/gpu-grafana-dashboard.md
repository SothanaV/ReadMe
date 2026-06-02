# NVIDIA GPU Grafana Dashboard Monitoring

Guide for setting up NVIDIA GPU monitoring using DCGM Exporter, Prometheus, and Grafana.

## Prerequisites

- NVIDIA GPU with supported architecture
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed on the host
- Docker or Docker Compose installed
- Prometheus installed and configured
- Grafana installed and configured

## Step 1: Deploy DCGM Exporter

DCGM (Data Center GPU Manager) Exporter collects GPU metrics and exposes them via a Prometheus-compatible endpoint.

Reference: [DCGM Exporter Documentation](https://docs.nvidia.com/datacenter/dcgm/latest/gpu-telemetry/dcgm-exporter.html)

### Docker Compose Configuration

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

### Verify the Metrics Endpoint

```bash
curl http://localhost:9400/metrics
```

## Step 2: Configure Prometheus

Add the DCGM Exporter as a scrape target in your Prometheus configuration (`prometheus.yml`):

```yaml
scrape_configs:
  - job_name: "nvidia-gpu"
    scrape_interval: 2s
    static_configs:
      - targets:
          - "<server-ip>:9400"
```

Replace `<server-ip>` with the actual IP address of the host running the exporter.

### Restart Prometheus

```bash
# If running as a Docker container
docker restart prometheus

# If managed by systemd
sudo systemctl restart prometheus
```

### Verify the Prometheus Target

Navigate to `http://<prometheus-ip>:9090/targets` and confirm the `nvidia-gpu` job shows a status of **UP**.

## Step 3: Import the Grafana Dashboard

### Option A: Import from Grafana.com

1. In Grafana, go to **Dashboards > Import**.
2. Enter dashboard ID `15117` in the "Import via grafana.com" field.
3. Click **Load**, select your Prometheus data source, and click **Import**.

Dashboard link: [15117 - NVIDIA DCGM Exporter](https://grafana.com/grafana/dashboards/15117-nvidia-dcgm-exporter/)

### Option B: Import a JSON File

1. Download the dashboard JSON from the link above.
2. In Grafana, go to **Dashboards > Import**.
3. Click **Upload JSON file** and select the downloaded file.
4. Select your Prometheus data source and click **Import**.

## Dashboard Features

The imported dashboard provides visibility into:

- GPU utilization and memory usage
- GPU temperature and thermal throttling
- GPU power consumption
- GPU clock frequencies
- ECC memory errors
- NVLink metrics (if supported by the GPU)

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| DCGM Exporter fails to start | Ensure NVIDIA Container Toolkit is installed and `nvidia-smi` works on the host |
| No metrics in Prometheus | Check that port `9400` is not blocked by a firewall; verify the target is UP in Prometheus |
| Grafana shows no data | Verify the Prometheus data source is correctly configured in Grafana |
| GPU metrics not appearing | Run `nvidia-smi` on the host to confirm GPU accessibility |

## References

- [DCGM Exporter Documentation](https://docs.nvidia.com/datacenter/dcgm/latest/gpu-telemetry/dcgm-exporter.html)
- [Grafana Dashboard 15117](https://grafana.com/grafana/dashboards/15117-nvidia-dcgm-exporter/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
