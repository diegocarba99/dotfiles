
#!/bin/bash
icon="$HOME/.config/i3/lockscreen/icon512.png" 
tmpbg='/tmp/screen.png'
scrot /tmp/screen.png
convert $tmpbg -scale 10% -scale 1000% $tmpbg
convert $tmpbg $icon -gravity center -composite -matte $tmpbg
i3lock -u -i $tmpbg
rm /tmp/screen.png



