#!/bin/bash
# ホームホルダー（pi)で実行する

#スクラッチのインストール
sudo apt update -y  
sudo apt upgrade -y

sudo apt install nodejs npm -y

mkdir scratch
cd scratch
git clone --depth 1 https://github.com/llk/scratch-vm.git
git clone --depth 1 https://github.com/llk/scratch-gui.git
cd scratch-vm
npm install
sudo npm link
cd ../scratch-gui
npm install
sudo npm link scratch-vm


#スクラッチ拡張のインストール(scratch_vm関連）

cd ~/scratch/scratch-vm/src/extensions
mkdir scratch3_newblocks
cd scratch3_newblocks
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/index/index.js > index.js
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/pyserver/pyserver.py > pyserver.py
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/newblocks.png > newblocks.png

#起動スクリプトのインストール
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/scratch.sh > scratch.sh
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/scratch2.sh > scratch2.sh

sudo chmod +x scratch.sh
sudo chmod +x scratch2.sh

curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/python.desktop > ~/Desktop/python.desktop
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/scratch.desktop > ~/Desktop/scratch.desktop

cd ~/scratch/scratch-vm/src/extension-support
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/index/extension-manager.js > extension-manager.js


cd ~/scratch/scratch-gui/src/lib/libraries/extensions
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/index.jsx > index.jsx
mkdir newblocks
cd newblocks
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/newblocks.png > newblocks.png
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/setting%20file/newblocks-small.png > newblocks-small.png

#slackサーバーのインストール
cd ~/scratch/scratch-vm/src/extensions/scratch3_newblocks
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/slack/slack_pass.txt > slack_pass.txt
curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/slack/slack_server.py > slack_server.py

pip install slack-bolt --break-system-packages

curl https://raw.githubusercontent.com/LineDrawRobot/scratch_project/refs/heads/main/slack/slack_server.service >slack_server.service
sudo mv slack_server.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable slack_server.service
sudo systemctl start slack_server.service

#SPI有効化
sudo raspi-config nonint do_spi 0

