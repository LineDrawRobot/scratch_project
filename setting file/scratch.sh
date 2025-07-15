#!/bin/bash
lxterminal -e "python ~/scratch/scratch-vm/src/extensions/scratch3_newblocks/pyserver.py; exec bash" &
lxterminal -e "cd ~/scratch/scratch-gui; yarn start; exec bash" &

if pgrep -f "chromium-browser" > /dev/null; then
    echo "すでにChromiumが開いています。起動しません。"
else
    echo "Chromiumを起動します。"
    sleep 2m
	chromium-browser http://localhost:8601
fi

