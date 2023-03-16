#!/usr/bin/env bash
: '
Copyright (c) 2022 KTH RPL
Author: Kin (https://kin-zhang.github.io/)
Date: 2023-03-16
Usage: Install glog and gflags automatically
RUN in terminal: `curl -sL https://raw.githubusercontent.com/Kin-Zhang/Kin-Zhang/main/Dockerfiles/latest_glog_gflag.sh | bash`
'

mkdir -p ~/workspace/tmp_lib
cd ~/workspace/tmp_lib
git clone https://github.com/google/glog.git && cd glog
mkdir build && cd build
cmake .. && make -j$(nproc)
make all install

cd ~/workspace/tmp_lib
git clone https://github.com/gflags/gflags.git
cd gflags
mkdir build && cd build
cmake .. -DBUILD_SHARED_LIBS=ON && make
make all install

rm -rf ~/workspace/tmp_lib
