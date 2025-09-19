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
import sys
import spidev

with open("slack_pass.txt", "r", encoding="utf-8") as f:
    app_token = f.readline().strip()
    bot_token = f.readline().strip()

# ボットトークンを渡してアプリを初期化します
app = App(token=bot_token)
global lock


count = 0
time_out = 10  # シリアル通信の再送信回数の上限

volume = 0
b = 1
G = 0
data = 0

pin_num = [5, 6, 13, 19, 26, 16, 20, 21, 25]  # 使用するgpioピン番号
n_pin = 9  # 使用するgpioピン数

str1 = '0'
op = {'inst': '0', 'ForB': '0', 'SPEED': '0', 'INOUT': '0',
      'CW': '0', 'ptn': '0', 'SIZE': '0', 'TIME': '0'}
timer1 = 0
index = 0

led_pin = {}
inst2 = {}

for i in range(n_pin):
    led_pin[i]=LED(pin_num[i])

# 'こんにちは' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html


def parse(path):

    qs = p.urlparse(path).query
    qs_d = p.parse_qs(qs)
    return qs_d


@app.message("ready")
def admin_process(message, say):
    global power
    channel = message["channel"]
    if channel == 'C094ZB5A458':
        power = 1
        print("power on")


@app.message("pause")
def admin_process(message, say):
    global power
    channel = message["channel"]
    if channel == 'C094ZB5A458':
        power = 0
        print("power off")


@app.message("instruction")
def message_hello(message, say):
    global lock, power
    if lock == 0 and power == 0:
        lock = 1
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

    # else:
        # print("block message")


def do_GET(path):

    inst = parse(path)
    for key in inst:
        op[key] = inst[key][0]

    if inst['inst'][0] == 'START':
        led_pin[0].on()
        print('START')

    elif inst['inst'][0] == 'STOP':
        for i in range(n_pin):
            led_pin[i].off()
        print('STOP')

    elif inst['inst'][0] == 'TIREON':
        print('TIREON')
        if op['ForB'] == '1':
            led_pin[2].on()
            time.sleep(timer1)
            led_pin[3].on()
            time.sleep(timer1)

        elif op['ForB'] == '0':
            led_pin[2].off()
            time.sleep(timer1)
            led_pin[3].off()
            time.sleep(timer1)

        if op['SPEED'] == '1':
            led_pin[4].off()
            time.sleep(timer1)
            led_pin[5].on()
            time.sleep(timer1)
            led_pin[6].off()
            time.sleep(timer1)
            led_pin[7].on()
            time.sleep(timer1)

        elif op['SPEED'] == '2':
            led_pin[4].on()
            time.sleep(timer1)
            led_pin[5].off()
            time.sleep(timer1)
            led_pin[6].on()
            time.sleep(timer1)
            led_pin[7].off()
            time.sleep(timer1)

        elif op['SPEED'] == '3':
            led_pin[4].on()
            time.sleep(timer1)
            led_pin[5].on()
            time.sleep(timer1)
            led_pin[6].on()
            time.sleep(timer1)
            led_pin[7].on()
            time.sleep(timer1)

    elif inst['inst'][0] == 'TIREOFF':
        print('TIREOFF')
        for i in range(1, 8):
            led_pin[i].off()
            time.sleep(timer1)

    elif inst['inst'][0] == 'POWDER':
        print('POWDER')
        if op['INOUT'] == '0':
            led_pin[1].off()
            time.sleep(timer1)
        elif op['INOUT'] == '1':
            led_pin[1].on()
            time.sleep(timer1)

    elif inst['inst'][0] == 'TURN':
        print('TURN')
        if op['CW'] == '0':
            led_pin[2].on()
            time.sleep(timer1)
            led_pin[3].off()
            time.sleep(timer1)

        elif op['CW'] == '1':
            led_pin[2].off()
            time.sleep(timer1)
            led_pin[3].on()
            time.sleep(timer1)

        if op['SPEED'] == '1':
            led_pin[4].off()
            time.sleep(timer1)
            led_pin[5].on()
            time.sleep(timer1)
            led_pin[6].off()
            time.sleep(timer1)
            led_pin[7].on()
            time.sleep(timer1)

        elif op['SPEED'] == '2':
            led_pin[4].on()
            time.sleep(timer1)
            led_pin[5].off()
            time.sleep(timer1)
            led_pin[6].on()
            time.sleep(timer1)
            led_pin[7].off()
            time.sleep(timer1)

        elif op['SPEED'] == '3':
            led_pin[4].on()
            time.sleep(timer1)
            led_pin[5].on()
            time.sleep(timer1)
            led_pin[6].on()
            time.sleep(timer1)
            led_pin[7].on()
            time.sleep(timer1)

        elif inst['inst'][0] == 'CIRCLE':
            led_pin[2].off()
            led_pin[3].off()
            if op['SIZE'] == '0':
                if op['CW'] == '0':
                    led_pin[4].off()
                    led_pin[5].off()
                    led_pin[6].on()
                    led_pin[7].off()
                elif op['CW'] == '1':
                    led_pin[4].on()
                    led_pin[5].off()
                    led_pin[6].off()
                    led_pin[7].off()

            elif op['SIZE'] == '1':
                if op['CW'] == '0':
                    led_pin[4].off()
                    led_pin[5].on()
                    led_pin[6].on()
                    led_pin[7].on()

                elif op['CW'] == '1':
                    led_pin[4].on()
                    led_pin[5].on()
                    led_pin[6].off()
                    led_pin[7].on()

            elif op['SIZE'] == '2':
                if op['CW'] == '0':
                    led_pin[4].off()
                    led_pin[5].on()
                    led_pin[6].on()
                    led_pin[7].off()

                elif op['CW'] == '1':
                    led_pin[4].on()
                    led_pin[5].off()
                    led_pin[6].off()
                    led_pin[7].on()

                """
                            elif op['ptn']=='2':
                                if op['CW']=='0':
                                    led_pin[4].on()
                                    led_pin[5].off()
                                    led_pin[6].on()
                                    led_pin[7].on()

                                elif op['CW']=='1':
                                    led_pin[4].on()
                                    led_pin[5].on()
                                    led_pin[6].on()
                                    led_pin[7].off()

                        elif op['SIZE']=='3':
                            if op['ptn']=='1':
                                if op['CW']=='0':
                                    led_pin[4].on()
                                    led_pin[5].off()
                                    led_pin[6].on()
                                    led_pin[7].on()

                                elif op['CW']=='1':
                                    led_pin[4].on()
                                    led_pin[5].on()
                                    led_pin[6].on()
                                    led_pin[7].off()

                            elif op['ptn']=='2':
                                if op['CW']=='0':
                                    led_pin[4].off()
                                    led_pin[5].on()
                                    led_pin[6].on()
                                    led_pin[7].off()

                                elif op['CW']=='1':
                                    led_pin[4].on()
                                    led_pin[5].off()
                                    led_pin[6].off()
                                    led_pin[7].on()
                """

    elif inst['inst'][0] == 'CIRCLE3':
        print('CIRCLE3')

        spi = spidev.SpiDev()
        spi.open(0, 0)  # SPI0, CE0
        spi.max_speed_hz = 115200
        spi.mode = 1  # SPI MODE 1
        t_size = int(op['turnsize'])
        i = 0

        tx_data = [0x00, 0x00]
        print("bb")
        tx_data[1] = t_size >> 8
        print("aa")
        tx_data[0] = t_size & 0xFF

        print(tx_data)
        rx_data = [0xFF, 0xFF]
        error = 0
        led_pin[8].on()

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
            rx_data = spi.xfer2([0x00, 0x00])  # ダミーデータを送信して、受信データ確認
            time.sleep(0.1)
            print(f"受信データ: {[f'{b:04X}' for b in rx_data]}")

            led_pin[8].off()
            spi.close()
            if (error == 1):
                print("Value setting is incomplete")
                return 1
        
            else:
                print("Value setting is complete")

            if op['CW'] == '0':
                led_pin[4].on()
                led_pin[5].off()
                led_pin[6].on()
                led_pin[7].on()

            elif op['CW'] == '1':
                led_pin[4].on()
                led_pin[5].on()
                led_pin[6].on()
                led_pin[7].off()

    elif inst['inst'][0] == 'SLEEP' or inst['inst'][0] == 'SLEEP_A':
        print('SLEEP')
        time.sleep(float(op['TIME']))


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


if __name__ == "__main__":
    # アプリを起動して、ソケットモードで Slack に接続します
    lock = 0
    power = 0
    SocketModeHandler(app, app_token).start()
