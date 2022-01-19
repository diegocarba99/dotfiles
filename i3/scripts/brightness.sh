#!/bin/bash

# BRIGHTNESS ADJUSTER
# This script calculates a brightness value depending on a previos
# saved value in a file. If the file doesn't exist the script
# automatically sets the initial value to %80 brightness
#
# Autor:
#       Diego Carballeda
#       diegocarballedamartinez@gmail.com
#       https://github.com/diegocarba99
# Version:
#       v1.0: 01/06/2020 - Basic functionality.


# Variables
brtlvl=1.0 # Brightness level
brtfile=/home/diego/.config/i3/scripts/brt.dat #File where brightness level is stored
screen=$(xrandr | grep " connected" | cut -f1 -d" ")


# Checking if the file exists. If it exists, gets the value
if [[ -f $brtfile ]]
then
    echo $brtfile exists. getting stored value
    brtlvl=$(cat $brtfile)
fi


# Calculation of new brightness level. Can either increase or decrease
if [ "$1" = '+' ]; then
    brtlvlnew=$(echo "$brtlvl + 0.05" | bc)
    if [ $(echo "$brtlvlnew>1.0" | bc) -eq 1 ]; then
        brtlvlnew='1.0'
    fi
elif [ "$1" = '-' ]; then
    brtlvlnew=$(echo "$brtlvl - 0.05" | bc)
    if [ $(echo "$brtlvl < 0.0" | bc) -eq 1 ]; then
        brtlvlnew='0.0'
    fi
fi


# Changing brightness level to newly calculated one
xrandr --output $screen --brightness $brtlvlnew;


# Ouputing control information
echo previous value: $brtlvl
echo new value     : $brtlvlnew


# Saving new brightness level to file
echo $brtlvlnew > $brtfile

