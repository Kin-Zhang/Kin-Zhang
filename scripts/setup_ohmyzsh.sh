#!/usr/bin/env bash
#
# oh-my-zsh setup scripts
#
#   Modify: Kin ZHANG (张清文) <https://kin-zhang.github.io/>
#   Copyright (C) 2022-now, RPL, KTH Royal Institute of Technology
#
#


# plugins
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions 
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting fzf)/" "${HOME}/.zshrc"

# theme change
printf '\n\r%s [Recommand to different from your laptop to server/nodes Say Y if so]\n\r Do you want to change default theme to zsh? [Y/n]%s ' \
"$FMT_YELLOW" "$FMT_RESET"
read -r opt
case $opt in
    y*|Y*|"")
        echo "Replacing from robbyrussell to lukerandall";
        sed -i "s/robbyrussell/lukerandall/" "${HOME}/.zshrc";
        sed -i "s/%2~/%d/" "${HOME}/.oh-my-zsh/themes/lukerandall.zsh-theme";
        echo "Done for theme changing to lukerandall, also show all the path" ;;
    n*|N*) echo "Keep the default theme: robbyrussell" ;;
    *) echo "Keep the default theme: robbyrussell" ;;
esac
