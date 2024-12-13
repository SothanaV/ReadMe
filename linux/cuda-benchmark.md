# Benchmark GPU
- requirement
    - nvidia gpu
    - nvidia driver
    - docker
    - nvidia-docker

- run nvidia-docker
```
docker  run --rm -it --gpus all nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04
```

- update and install package
```
apt update && apt install -y git build-essential
```

- clone repo
```
git clone https://github.com/NVIDIA/cuda-samples.git
```

- run benchmark
```
cd cuda-samples/Samples/4_CUDA_Libraries/matrixMulCUBLAS
make
./matrixMulCUBLAS
```