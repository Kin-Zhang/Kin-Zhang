#!/usr/bin/env bash
#
# dochat.sh - Docker WeChat for Linux
#
#   Author: Huan (李卓桓) <zixia@zixia.net>
#   Modify: Kin (张清文) <kin_eng@163.com>
#   Copyright (c) 2020-now
#
#   License: Apache-2.0
#   GitHub: https://github.com/huan/docker-wechat
#
set -eo pipefail

function hello () {
  cat <<'EOF'

       ____         ____ _           _
      |  _ \  ___  / ___| |__   __ _| |_
      | | | |/ _ \| |   | '_ \ / _` | __|
      | |_| | (_) | |___| | | | (_| | |_
      |____/ \___/ \____|_| |_|\__,_|\__|

      https://github.com/huan/docker-wechat

                +--------------+
               /|             /|
              / |            / |
             *--+-----------*  |
             |  |           |  |
             |  |   盒装    |  |
             |  |   微信    |  |
             |  +-----------+--+
             | /            | /
             |/             |/
             *--------------*

      DoChat /dɑɑˈtʃæt/ (Docker-weChat) is:

      📦 a Docker image
      🤐 for running PC Windows WeChat
      💻 on your Linux desktop
      💖 by one-line of command

EOF
}

function pullUpdate () {
  if [ -n "$DOCHAT_SKIP_PULL" ]; then
    return
  fi

  echo '🚀 Pulling the docker image...'
  echo
  docker pull zhangkin/wechat:rm
  echo
  echo '🚀 Pulling the docker image done.'
}

function main () {

  hello
  # pullUpdate

  OPTIONS=()

  if [ -f /dev/snd ]; then
    OPTIONS+=('--device' '/dev/snd')
  fi
  if [ -f /dev/video0 ]; then
    OPTIONS+=('--device' '/dev/video0')
  fi
  if [[ $(lshw -C display | grep vendor) =~ NVIDIA ]]; then
    OPTIONS+=('--gpus' 'all' '--env' 'NVIDIA_DRIVER_CAPABILITIES=all')
  fi

  echo '🚀 Starting DoChat /dɑɑˈtʃæt/ ...'
  echo

  # Issue #111 - https://github.com/huan/docker-wechat/issues/111
  rm -f "$HOME/DoChat/Applcation Data/Tencent/WeChat/All Users/config/configEx.ini"

  #
  # --privileged: enable sound (/dev/snd/)
  # --ipc=host:   enable MIT_SHM (XWindows)
  # https://phoenixnap.com/kb/docker-run-override-entrypoint
  # -it --entrypoint /bin/bash zhangkin/wechat:rm   
  docker run --device /dev/snd --name DoChat_kin --ipc="host" \
    -v "$HOME/WeChatFiles":"/WeChatFiles" \
    -v "$HOME/DoChat/Applcation Data":'/.wine/drive_c/users/user/Application Data/' \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=unix$DISPLAY \
    -e XMODIFIERS=@im=fcitx \
    -e XMODIFIERS=@im=fcitx \
    -e QT_IM_MODULE=fcitx \
    -e GTK_IM_MODULE=fcitx \
    -e AUDIO_GID=`getent group audio | cut -d: -f3` \
    -e GID="$(id -g)" \
    -e UID="$(id -u)" \
    -e DOCHAT_DEBUG \
    -e DOCHAT_DPI \
    --privileged \
    --entrypoint ./entrypoint.sh zhangkin/wechat:rm

    echo
    echo "📦 DoChat Exited with code [$?]"
    echo
    echo '🐞 Bug Report: https://github.com/huan/docker-wechat/issues'
    echo

}

main
