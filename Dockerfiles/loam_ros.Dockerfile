FROM osrf/ros:melodic-desktop-full
LABEL maintainer="Kin Zhang <kin_eng@163.com>"

# Just in case we need it
ENV DEBIAN_FRONTEND noninteractive

# install zsh
RUN apt update && apt install -y wget git zsh tmux vim g++ unzip libparmetis-dev
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p git \
    -p ssh-agent \
    -p https://github.com/agkozak/zsh-z \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting

RUN wget -O /root/gtsam.zip https://github.com/borglab/gtsam/archive/4.0.0-alpha2.zip
RUN cd /root/ && unzip gtsam.zip -d /root/
WORKDIR /root/gtsam-4.0.0-alpha2/
RUN mkdir build && cd build && cmake .. && make install

# kin self vdbfusion_mapping
RUN echo "source /opt/ros/melodic/setup.zsh" >> ~/.zshrc
RUN echo "source /opt/ros/melodic/setup.bashrc" >> ~/.bashrc

RUN mkdir -p /workspace/LeGO_LOAM_ws /workspace/data
WORKDIR /workspace/LeGO_LOAM_ws
# RUN git clone https://gitee.com/caomengnb/LeGO-LOAM.git /workspace/LeGO_LOAM_ws/src
RUN git clone https://gitee.com/caomengnb/SC-LeGO-LOAM.git /workspace/LeGO_LOAM_ws/src

# ================> Following is A-LOAM
# install glog gflag
RUN curl -sL https://raw.githubusercontent.com/Kin-Zhang/Kin-Zhang/main/Dockerfiles/setup_lib.sh | bash

RUN cd / && git clone --depth 1 --branch 1.14.0 https://ceres-solver.googlesource.com/ceres-solver \
    && cd ceres-solver && mkdir build && cd build && cmake .. \
    && make -j$(nproc) \
    && make -j$(nproc) all install \
    && cd / \
    && rm -rf /ceres-solver