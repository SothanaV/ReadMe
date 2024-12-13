# Benchmark GPU
- requirement
    - nvidia gpu
    - nvidia driver
    - docker
    - nvidia-docker

- run nvidia-docker
```bash
docker  run --rm -it --gpus all nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04
```

- update and install package
```bash
apt update && apt install -y git build-essential
```

- clone repo
```bash
git clone https://github.com/NVIDIA/cuda-samples.git
```

- run benchmark
```bash
cd cuda-samples/Samples/4_CUDA_Libraries/matrixMulCUBLAS
make
./matrixMulCUBLAS
```

- output like this
```bash
root@5251c11c5cdc:/cuda-samples/Samples/4_CUDA_Libraries/matrixMulCUBLAS# ./matrixMulCUBLAS
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