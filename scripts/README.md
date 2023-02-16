Scripts
---

For blog usage, please read corresponding blogs


1. [wechat.sh](wechat.sh): using docker+wine to install wechat on ubuntu, read zhihu here [Ubuntu 安装使用微信 wechat (docker+wine) 详细教程](https://zhuanlan.zhihu.com/p/570187823) and reference is attached at code scripts and blog
2. [setup_ohmyzsh.sh](setup_ohmyzsh.sh): check [following](#oh-my-zsh)

3. TODO



### oh-my-zsh

Install oh my zsh and setup all the thing you need

Dependencies but most of computer should already have these things..
```bash
apt update && apt install curl git vim zsh
```

install oh-my-zsh, you need enter yes/no for some settings
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

setup on autosuggestions, highlighting, fzf [CTRL+R to view history]
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Kin-Zhang/Kin-Zhang/main/scripts/setup_ohmyzsh.sh)"
```

Demo here:

![img](https://img-blog.csdnimg.cn/5d3095910235457eaa369a2fb3c10bd0.gif)
