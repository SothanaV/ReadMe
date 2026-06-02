# GPU Benchmark with CUDA

Benchmark an NVIDIA GPU using the CUBLAS matrix multiplication sample from the CUDA Samples repository.

## Table of Contents

- [Requirements](#requirements)
- [Run the CUDA Container](#run-the-cuda-container)
- [Install Build Dependencies](#install-build-dependencies)
- [Clone CUDA Samples](#clone-cuda-samples)
- [Build and Run the Benchmark](#build-and-run-the-benchmark)
- [Example Output](#example-output)

---

## Requirements

- NVIDIA GPU
- NVIDIA driver installed on the host
- Docker
- NVIDIA Container Toolkit (`nvidia-docker`)

---

## Run the CUDA Container

Launch an interactive CUDA development container with GPU access:

```bash
docker run --rm -it --gpus all nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04
```

---

## Install Build Dependencies

Inside the container, install Git and the C++ build tools:

```bash
apt update && apt install -y git build-essential
```

---

## Clone CUDA Samples

```bash
git clone https://github.com/NVIDIA/cuda-samples.git
```

---

## Build and Run the Benchmark

Navigate to the CUBLAS matrix multiplication sample, build it, and run it:

```bash
cd cuda-samples/Samples/4_CUDA_Libraries/matrixMulCUBLAS
make
./matrixMulCUBLAS
```

---

## Example Output

```text
[Matrix Multiply CUBLAS] - Starting...
GPU Device 0: "Volta" with compute capability 7.0

GPU Device 0: "Tesla V100-SXM2-32GB" with compute capability 7.0

MatrixA(640,480), MatrixB(480,320), MatrixC(640,320)
Computing result using CUBLAS...done.
Performance= 5333.33 GFlop/s, Time= 0.037 msec, Size= 196608000 Ops
Computing result using host CPU...done.
Comparing CUBLAS Matrix Multiply with CPU results: PASS

NOTE: The CUDA Samples are not meant for performance measurements. Results may vary when GPU Boost is enabled.
```

**Key result:** 5,333 GFlop/s on a Tesla V100-SXM2-32GB (Volta, compute capability 7.0).
