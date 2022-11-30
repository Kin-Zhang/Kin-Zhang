#!/usr/bin/env bash
: '
Copyright (c) 2022 HKUST IADC
Author: Kin (kin_eng@163.com)
Date: 2022-06-17
Usage: Install glog and gflags automatically
RUN in terminal: `curl -sL https://raw.githubusercontent.com/Kin-Zhang/Kin-Zhang/main/Dockerfiles/setup_lib.sh | bash`
'

mkdir -p ~/workspace/tmp_lib
cd ~/workspace/tmp_lib
git clone https://github.com/google/glog.git
cd glog
git fetch --all --tags
git checkout tags/v0.4.0 -b v0.4.0
mkdir build && cd build
cmake .. && make -j$(nproc)
make install

cd ~/workspace/tmp_lib
git clone https://github.com/gflags/gflags.git
cd gflags
mkdir build && cd build
cmake .. -DBUILD_SHARED_LIBS=ON && make
make install

rm -rf ~/workspace/tmp_lib
