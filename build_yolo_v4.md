# Build Yolo V4
## prepair
    $ sudo apt-get install libopencv-core-dev
#
## build
    $ git clone https://github.com/AlexeyAB/darknet.git
    # edit Makefile
    $ make

## run
    # demo
    ./darknet detector demo cfg/coco.data cfg/yolov4.cfg yolov4.weights