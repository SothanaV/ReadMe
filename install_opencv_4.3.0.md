# install OpenCv 4.3.0
## prepair
    $ sudo apt-get install libopencv-dev
## install
    $ wget https://github.com/opencv/opencv/archive/4.3.0.zip
    $ unzip 4.3.0.zip && rm -rf 4.3.0.zip && mv opencv-4.3.0 OpenCV && cd OpenCV
    $ mkdir build && cd build
    $ cmake -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON -DENABLE_PRECOMPILED_HEADERS=OFF -DOPENCV_GENERATE_PKGCONFIG=ON ..
    $ make -j12
    $ sudo make install
    $ sudo ldconfig