# Install OpenCV 4.3.0 from Source

> **Archived** — Instructions for building OpenCV 4.3.0 with contrib modules from source on Ubuntu.

## Prerequisites

Install all build dependencies:

```bash
sudo apt-get install -y \
    wget git pkg-config build-essential cmake \
    zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev \
    libopenexr-dev libgdal-dev \
    libavcodec-dev libavformat-dev libswscale-dev \
    libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm \
    libopencore-amrnb-dev libopencore-amrwb-dev \
    libv4l-dev libxine2-dev \
    libtbb-dev libeigen3-dev \
    python-dev python-tk python-numpy \
    python3-dev python3-tk python3-numpy python3-pip \
    unzip wget \
    qt5-default libvtk6-dev libopencv-dev \
    libgl-dev libglu-dev libglib2.0-dev \
    libsm-dev libxrender-dev libfontconfig1-dev libxext-dev \
    doxygen opencv-data
```

## Download Source

Download OpenCV and the contrib modules, both at version 4.3.0:

```bash
# Download and extract OpenCV
wget https://github.com/opencv/opencv/archive/4.3.0.zip
unzip 4.3.0.zip
rm 4.3.0.zip
mv opencv-4.3.0 OpenCV

# Download and extract opencv_contrib
wget https://github.com/opencv/opencv_contrib/archive/4.3.0.zip
unzip 4.3.0.zip
rm 4.3.0.zip
```

## Build and Install

```bash
cd OpenCV
mkdir build && cd build

cmake \
    -DWITH_QT=ON \
    -DWITH_OPENGL=ON \
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON \
    -DENABLE_PRECOMPILED_HEADERS=OFF \
    -DOPENCV_GENERATE_PKGCONFIG=ON \
    -DINSTALL_PYTHON_EXAMPLES=ON \
    -DPYTHON_DEFAULT_EXECUTABLE=$(which python3) \
    -DWITH_PTHREADS_PF=ON \
    -DWITH_OPENMP=ON \
    -DWITH_IPP=ON \
    ..

# Adjust -j flag to match the number of CPU cores available
make -j$(nproc)

sudo make install
sudo ldconfig
```

## Verify Installation

```python
import cv2
print(cv2.__version__)
```

## References

- [OpenCV Official Documentation](https://docs.opencv.org/4.3.0/)
- [OpenCV Releases](https://github.com/opencv/opencv/releases)
