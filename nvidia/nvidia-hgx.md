# NVIDIA HGX on Kubernetes

Step-by-step guide to prepare an NVIDIA HGX node (NVLink/NVSwitch baseboard) and expose its GPUs to Kubernetes workloads.

Unlike a standard PCIe GPU server, an HGX system requires the **NVIDIA Fabric Manager** to bring up the NVSwitch fabric before any GPU can be used. Skipping this step causes `nvidia-smi` to hang or report "ERR!" for every GPU.

## Prerequisites

- Ubuntu 20.04 / 22.04 / 24.04 on an HGX baseboard (H100, A100, A800, HGX-2, etc.)
- `nvidia-fabricmanager` package matching the driver version
- Kubernetes cluster with `containerd` as the runtime
- `kubectl` configured with cluster-admin access

> [!IMPORTANT]
> The driver, utils, and fabric manager packages **must be the exact same version** (e.g. all `580`). A mismatch causes the fabric manager to refuse to start.

## Step 1: Install Driver, Utils, and Fabric Manager

Install all three packages in a single `apt` invocation so the versions stay in sync.

```bash
sudo apt update
sudo apt install -y \
  nvidia-driver-580-server \
  nvidia-utils-580-server \
  nvidia-fabricmanager-580
```

- `nvidia-driver-580-server` — kernel driver and `nvidia.ko` modules
- `nvidia-utils-580-server` — `nvidia-smi` and supporting tools
- `nvidia-fabricmanager-580` — manages the NVSwitch fabric on HGX baseboards

## Step 2: Load Kernel Modules

Load the modules manually if you cannot reboot immediately after install.

```bash
sudo modprobe nvidia
sudo modprobe nvidia-uvm
sudo nvidia-modprobe -u -c 0
```

To persist across reboots, add the modules to `/etc/modules-load.d/nvidia.conf`:

```text
nvidia
nvidia-uvm
```

## Step 3: Start the Fabric Manager

The Fabric Manager must be running **before** any process opens a GPU.

```bash
sudo systemctl enable --now nvidia-fabricmanager
```

If the service fails with `NV_ERR_FABRIC_STATE_OUT_OF_SYNC`, reboot the node — the fabric state is only rebuilt cleanly at boot.

## Step 4: Verify the GPU Stack

```bash
# Driver and GPUs visible
nvidia-smi

# Fabric Manager active and healthy
systemctl status nvidia-fabricmanager
```

`nvidia-smi` should list every GPU on the baseboard with no `ERR!` entries. On an 8-GPU HGX node you should see all eight GPUs, and NVLink status should show as active.

## Step 5: Install the NVIDIA Container Toolkit

Reference: [NVIDIA Container Toolkit install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### Add the Repository

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

### Install the Toolkit

```bash
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
```

### Configure containerd and Restart

```bash
sudo nvidia-ctk runtime configure --runtime=containerd
sudo systemctl restart containerd
```

This appends an `nvidia` runtime block to `/etc/containerd/config.toml`. Verify with:

```bash
sudo nvidia-ctk runtime configure --runtime=containerd --dry-run
```

## Step 6: Deploy the NVIDIA Device Plugin

The device plugin advertises `nvidia.com/gpu` as a schedulable resource on each node.

```bash
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.16.0/deployments/static/nvidia-device-plugin.yml
```

For an HGX node where you want all GPUs on a single node to share one NVLink domain (required for multi-GPU training), make sure the plugin is **not** running in MIG or time-slicing mode.

### Verify GPUs Are Advertised

```bash
kubectl get nodes \
  "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
```

The HGX node should report `8` (or the number of GPUs on the baseboard).

## Step 7: Test Pod

Request GPUs with `nvidia.com/gpu` in the pod's resource limits.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-test-pod
spec:
  restartPolicy: Never
  containers:
    - name: cuda-container
      image: nvcr.io/nvidia/cuda:12.4.1-base-ubuntu22.04
      command: ["nvidia-smi"]
      resources:
        limits:
          nvidia.com/gpu: 1
```

```bash
kubectl apply -f gpu-test-pod.yaml
kubectl logs -f gpu-test-pod
```

Expected output is a normal `nvidia-smi` table showing the assigned GPU.

To test the full NVLink domain (all 8 GPUs on one HGX node), request `nvidia.com/gpu: 8` and run `nvidia-smi topo -m` inside the pod — every pair should be connected via `NV#` (NVLink), not `PHB` or `SYS`.

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `nvidia-smi` hangs or shows `ERR!` | Fabric Manager not running; start `nvidia-fabricmanager` and reboot if state is out of sync |
| `Failed to initialize NVML` in a container | Container Toolkit not configured for `containerd`; re-run `nvidia-ctk runtime configure` and restart `containerd` |
| Node reports `0` GPUs | Device plugin pod is crash-looping — `kubectl logs -n kube-system -l name=nvidia-device-plugin-ds` |
| `nvmlErrorString=GPU is lost` after a reboot | Power-cycle the baseboard; NVSwitch state can be lost on hard power events |
| Multi-GPU job falls back to PCIe | Pod requested fewer than all GPUs on the node, or the plugin is configured with `--fail-on-init-error=false` masking a fabric failure |

## References

- [NVIDIA Fabric Manager User Guide](https://docs.nvidia.com/datacenter/tesla/fabric-manager-user-guide/index.html)
- [NVIDIA Container Toolkit Install Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [NVIDIA Device Plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin)
- [GPU Operator (alternative all-in-one install)](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)
