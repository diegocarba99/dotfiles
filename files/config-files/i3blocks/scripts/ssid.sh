#!/bin/bash

# Name of the wifi network
echo "$(iw dev wlan0 link | grep SSID | cut -d " " -f 2-)"

# Get signal level 
signal_lvl=$(iw dev wlan0 link | grep signal | cut -d " " -f 2)
echo $signal_lvl

# Set default color. Blue
quality="#80b5ff"

# white (-30, -59] --> excellent signal
if [[ $signal_lvl -gt -60 ]]; then 
    quality="#ffffff"
# green [-60, -66] --> good signal
elif [[ $signal_lvl -gt -67 ]]; then
    quality="#80ffaa"
# green/yellow [-67, -69] --> reliable signal
elif [[ $signal_lvl -gt -70 ]]; then
    quality="#c8ff80"
# yellow [-70, -79] --> not strong signal
elif [[ $signal_lvl -gt -80 ]]; then
    quality="#fffd80"
# orange [-80, -89] --> unreliable signal
elif [[ $signal_lvl -gt -90 ]]; then
    quality="#ffae70"
# red [-90, +) --> bad signal
elif [[ $signal_lvl -le -91 ]]; then
    quality="#ff7070"
fi

#Return color value
echo $quality

exit 0
