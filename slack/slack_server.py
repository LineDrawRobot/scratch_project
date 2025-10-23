import os
import time
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as p
import requests
from gpiozero import LED
from gpiozero import Button
import sys
import spidev
import traceback
import datetime


with open("/home/pi/scratch/scratch-vm/src/extensions/scratch3_newblocks/slack_pass.txt", "r", encoding="utf-8") as f:
    app_token = f.readline().strip()
    bot_token = f.readline().strip()

# ボットトークンを渡してアプリを初期化します
app = App(token=bot_token)
global lock


count = 0
time_out = 5  # シリアル通信の再送信回数の上限

volume = 0
b = 1
G = 0
data = 0

###################GPIO#################################
power = LED(22) #電源制御
serial = LED(25)#シリアル制御
execute = LED(23)#動作開始
power_program = LED(17)#このプログラムが起動しているかチェック用

execute_end =Button(24, pull_up=False)


#################変数関連######################################

op = {'inst': '0', 'ForB': '0', 'DISTANCE': '0', 'INOUT': '0',
      'CW': '0', 'RADIUS': '0', 'ANGLE': '0'}
wait_time = 0
index = 0
global powder_flag
###############scratchから送られたメッセージを解析##################
def parse(path):

    qs = p.urlparse(path).query
    qs_d = p.parse_qs(qs)
    return qs_d

###############slackに投稿されたメッセージを取得##################
@app.message("instruction")
def message_hello(message, say):
    global lock, powder_flag
    ###過去のメッセージを無視する
    event_ts = float(message.get("ts", 0))
    now_ts = time.time()
    if now_ts - event_ts > 5:
        print(f"[INFO] Skipping old message: {message.get('text')} (ts={event_ts})")
        return
    ###動作中に来たメッセージを無視する
    if  lock == 1:
        print("block message")
        return
        
    ###メッセージを取得
    lock = 1
    powder_flag = 0
    text = message["text"]
    text2 = re.sub('instruction|amp;|<|>', '', text)
    lines = text2.split('\n')
    print("動作開始")
    for item in lines:
        if item != '':
            n = do_GET(item)
            if (n == 1):
                break

    print("動作完了")
    lock = 0
    
def reset_pin():
    power.off()
    serial.off()
    execute.off()
    power_program.off()

def execute_instruction():
    execute.on()
    print("start instruction")
    while not execute_end.is_pressed:
        time.sleep(0.1)
    print("finish instruction")    
    execute.off()
    while execute_end.is_pressed:
        time.sleep(0.1)

def serial_send(data1,data2,data3):
    try:
        print(data1)
        print(data2)
        print(data3)
        spi = spidev.SpiDev()
        spi.open(0, 0)  # SPI0, CE0
        spi.max_speed_hz = 115200
        spi.mode = 1  # SPI MODE 1
        i = 0

        tx_data = [0x00, 0x00, 0x00,0x00,0x00]
        tx_data[4] = data3 >> 8
        tx_data[3] = data3 & 0xFF
        tx_data[2] = data2 >> 8
        tx_data[1] = data2 & 0xFF
        tx_data[0] = data1;
   
        
        print(tx_data)
        rx_data = [0xFF, 0xFF, 0xFF,0xFF, 0xFF]
        error = 0
        serial.on()

        while (tx_data != rx_data):
            if (i > time_out):
                error = 1
                break
            i += 1
            tx_data2 = tx_data[:]
            print(f"送信データ: {[f'{b:04X}' for b in tx_data]}")
            time.sleep(0.1)
            rx_data = spi.xfer2(tx_data2)  # SPI通信でデータ送信
            time.sleep(0.1)
            rx_data = spi.xfer2([0x00, 0x00, 0x00,0x00,0x00])  # ダミーデータを送信して、受信データ確認
            time.sleep(0.1)
            print(f"受信データ: {[f'{b:04X}' for b in rx_data]}")
        
        
        serial.off()
        spi.close()
        
        if (error == 1):
            
            raise Exception("Value setting is incomplete")
        
        else:
            print("Value setting is complete")
            
    except Exception as e:  
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ログに書き込む内容
        log_text = f"[{now}] {repr(e)}\n{traceback.format_exc()}\n"

        # ファイルに追記モードで書き込み
        with open("/home/pi/scratch/scratch-vm/src/extensions/scratch3_newblocks/log.txt", "a", encoding="utf-8") as f:
            f.write(log_text)
        reset_pin()
        os._exit(1)       


def do_GET(path):
  try:
    global powder_flag
    inst = parse(path)
    for key in inst:
        op[key] = inst[key][0]

    if inst['inst'][0] == 'START':
        power.on()
        print('START')

    elif inst['inst'][0] == 'STOP':
        power.off()
        print('STOP')

    elif inst['inst'][0] == 'TIREON':
        print('TIREON')
        
        ###シリアル通信開始#####
        if   op['ForB'] == '0' and powder_flag == 0:#前進・粉なし
            data1 = int(1)
        elif op['ForB'] == '0' and powder_flag == 1:#前進・粉あり
            data1 = int(2) 
        elif op['ForB'] == '1' and powder_flag == 0:#後退・粉なし
            data1 = int(3)
        elif op['ForB'] == '1' and powder_flag == 1:#後退・粉あり
            data1 = int(4)
             
        data2 = int(op['DISTANCE'])
        data3 = int(0)
        
        serial_send(data1, data2, data3)
        
        ###動作開始#####
        execute_instruction()


    elif inst['inst'][0] == 'TIREOFF':
        print('TIREOFF')


    elif inst['inst'][0] == 'POWDER':
        print('POWDER')
        powder_flag = int(op['INOUT']) #0:出さない   1:出す

    elif inst['inst'][0] == 'TURN':
        print('TURN')
        ###シリアル通信開始#####
        if   op['CW'] == '0' and powder_flag == 0:#時計回り・粉なし
            data1 = int(5)
        elif op['CW'] == '0' and powder_flag == 1:#時計回り・粉あり
            data1 = int(6) 
        elif op['CW'] == '1' and powder_flag == 0:#反時計回り・粉なし
            data1 = int(7)
        elif op['CW'] == '1' and powder_flag == 1:#反時計回り・粉あり
            data1 = int(8)
             
        data2 = int(op['ANGLE'])#回転角度
        data3 = int(0)
        
        serial_send(data1, data2, data3)
        
        ###動作開始#####
        execute_instruction()


    elif inst['inst'][0] == 'CIRCLE':
        print('CIRCLE3')
        ###シリアル通信開始#####
        if   op['CW'] == '0' and powder_flag == 0:#時計回り・粉なし
            data1 = int(9)
        elif op['CW'] == '0' and powder_flag == 1:#時計回り・粉あり
            data1 = int(10) 
        elif op['CW'] == '1' and powder_flag == 0:#反時計回り・粉なし
            data1 = int(11)
        elif op['CW'] == '1' and powder_flag == 1:#反時計回り・粉あり
            data1 = int(12)
             
        data2 = int(op['ANGLE'])#中心角度
        data3 = int(op['RADIUS'])#半径
        
        serial_send(data1, data2, data3)
        
        ###動作開始#####
        execute_instruction()
            
       
        
  except Exception as e:  
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ログに書き込む内容
    log_text = f"[{now}] {repr(e)}\n{traceback.format_exc()}\n"

    # ファイルに追記モードで書き込み
    with open("/home/pi/scratch/scratch-vm/src/extensions/scratch3_newblocks/log.txt", "a", encoding="utf-8") as f:
        f.write(log_text)
    reset_pin()
    os._exit(1)


if __name__ == "__main__":
    # アプリを起動して、ソケットモードで Slack に接続します
    lock = 0
    power_program.on()
    SocketModeHandler(app, app_token).start()
    power_program.off()
