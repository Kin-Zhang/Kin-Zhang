FROM node:lts
# https://github.com/facebook/docusaurus/issues/8026
LABEL maintainer="Kin Zhang <kin_eng@163.com>"

# Just in case we need it
ENV DEBIAN_FRONTEND noninteractive

# install zsh
RUN apt update && apt install -y wget git zsh tmux vim g++
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p git \
    -p ssh-agent \
    -p https://github.com/agkozak/zsh-z \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting

WORKDIR /docusaurus


# run to start container
# docusaurus can be downloaded here: https://github.com/facebook/docusaurus/releases
# docker run -it --net=host -v /home/kin/Documents/Wiki/docusaurus-2.3.1:/docusaurus --name wiki_docs zhangkin/docusaurus /bin/zsh
# inside the container
# yarn install & npm start

