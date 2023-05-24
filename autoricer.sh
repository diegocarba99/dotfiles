#!/bin/bash

# Author: Diego Carballeda
# This script, simple though it is, will install i3-gaps, sxhkd, and install my rice

#Dependencies and i3-Gaps
if command -v apt &> /dev/null
then
	sudo apt install sxhkd rofi i3 i3lock polybar fonts-font-awesome picom git flameshot
fi

#Download Rice
cd $HOME
git clone https://github.com/diegocarba99/dotfiles.git

#Moving Stuff
cd dotfiles
cp -r i3 ~/.config
cp .tmux.conf ~/.tmux.conf
cd && rm -r i3stuff

echo "Reboot or Log out"
