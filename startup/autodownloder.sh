#!/bin/bash
cd ~/scratch/scratch-vm/src/extensions/scratch3_newblocks
if ! curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/index/index.js > index.tmp
then
echo "DL失敗しました"
rm index.tmp
else
echo "DL成功しました"
mv index.tmp index.js
fi

if ! curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/pyserver/pyserver.py > pyserver.tmp
then
echo "DL失敗しました"
rm pyserver.tmp
else
echo "DL成功しました"
mv pyserver.tmp pyserver.py
fi

python init.py