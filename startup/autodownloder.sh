#!/bin/bash
cd ~/scratch/scratch-vm/src/extensions/scratch3_newblocks
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/index/index.js > index.js
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/pyserver/pyserver.py > pyserver.py
python init.py