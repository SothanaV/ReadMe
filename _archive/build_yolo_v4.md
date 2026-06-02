# Build YOLOv4 (Darknet)

> **Archived** — Instructions for building YOLOv4 from the AlexeyAB Darknet fork.

## Prerequisites

Install the required OpenCV development library:

```bash
sudo apt-get install libopencv-core-dev
```

> For full GPU-accelerated builds, also install CUDA, cuDNN, and the full OpenCV library before compiling.

## Build

Clone the repository, edit the `Makefile` to enable the desired options (GPU, CUDNN, OPENCV), then compile:

```bash
git clone https://github.com/AlexeyAB/darknet.git
cd darknet

# Edit Makefile to set GPU=1, CUDNN=1, OPENCV=1 as needed
nano Makefile

make
```

### Common Makefile Flags

```makefile
GPU=1       # Enable CUDA GPU support
CUDNN=1     # Enable cuDNN acceleration
OPENCV=1    # Enable OpenCV (required for video/camera input)
```

## Download Weights

```bash
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
```

## Run

### Object Detection on an Image

```bash
./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights data/dog.jpg
```

### Real-time Demo (Webcam or Video)

```bash
./darknet detector demo cfg/coco.data cfg/yolov4.cfg yolov4.weights
```

### Demo from a Video File

```bash
./darknet detector demo cfg/coco.data cfg/yolov4.cfg yolov4.weights input.mp4
```

## References

- [AlexeyAB Darknet Repository](https://github.com/AlexeyAB/darknet)
- [YOLOv4 Paper](https://arxiv.org/abs/2004.10934)
