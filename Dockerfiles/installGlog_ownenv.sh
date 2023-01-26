#!/usr/bin/env bash
: '
Copyright (c) 2022 KTH RPL
Author: Kin (kin_eng@163.com)
Date: 2022-12-23
Usage: Install glog and gflags automatically
RUN in terminal: `curl -sL https://raw.githubusercontent.com/Kin-Zhang/Kin-Zhang/main/Dockerfiles/setup_lib.sh | bash`
'

mkdir -p $HOME/workspace/tmp_lib
cd $HOME/workspace/tmp_lib
git clone https://github.com/google/glog.git
cd glog
git fetch --all --tags
git checkout tags/v0.4.0 -b v0.4.0
rm -rf build
mkdir build && cd build
cmake .. && make -j$(nproc)
sudo make install

cd $HOME/workspace/tmp_lib
git clone https://github.com/gflags/gflags.git
cd gflags
rm -rf build
mkdir build && cd build
cmake .. -DBUILD_SHARED_LIBS=ON && make
sudo make install

rm -rf ~/workspace/tmp_lib
