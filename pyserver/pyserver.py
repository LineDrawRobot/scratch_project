"""
円を描くの追加
すり合わせに伴い、円の大きさ（大中小）の数値を変更
不要な部分の削減
円の大きさ間違えてたから直せ
"""
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as p
import requests
import re
import time
from gpiozero import LED
import sys
import spidev


count = 0
time_out = 10 #シリアル通信の再送信回数の上限

volume=0
b=1
G=0
data=0

pin_num=[5,6,13,19,26,16,20,21,25] #使用するgpioピン番号
n_pin=9 #使用するgpioピン数

str1='0'
op = {'inst': '0','ForB': '0','SPEED': '0','CW':'0','ptn':'0','SIZE':'0'}
timer1=0
index=0

led_pin={}
inst2={}
for i in range(n_pin):
    led_pin[i]=LED(pin_num[i])



def parse(path):
    
    qs = p.urlparse(path).query
    qs_d = p.parse_qs(qs)
    return qs_d

class Server_class(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            global index
            print(index)
            global op
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            inst=parse(self.path)
            if inst['inst'][0]=='RESET':
                index=0;
                
            elif inst['inst'][0]=='EXECUTE':
                error=0
                for i in range(0,index):
                    inst = inst2[i]
                    if (error==1):
                        for i in range(n_pin):
                            led_pin[i].off()
                        print('ERROR')
                        break
                    
                    if inst['inst'][0]=='START':
                        led_pin[0].on()
                        print('START')
                    
                    elif inst['inst'][0]=='STOP':
                        for i in range(n_pin):
                            led_pin[i].off()                  
                        print('STOP')
                    

                    elif inst['inst'][0]=='TIREON':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                        if op['ForB']=='1':
                            led_pin[2].on()
                            time.sleep(timer1)
                            led_pin[3].on()
                            time.sleep(timer1)
                                    
                            if op['SPEED']=='1':
                                led_pin[4].off()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].off()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)
                                    
                            elif op['SPEED']=='2':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].off()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].off()
                                time.sleep(timer1)

                            elif op['SPEED']=='3':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)
                            
                        elif op['ForB']=='0':
                            led_pin[2].off()
                            time.sleep(timer1)
                            led_pin[3].off()
                            time.sleep(timer1)
                                    
                            if op['SPEED']=='1':
                                led_pin[4].off()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].off()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)
                                    
                            elif op['SPEED']=='2':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].off()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].off()
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='3':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)

                    elif inst['inst'][0]=='TIREOFF':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                            
                        for i in range(2,8):
                            led_pin[i].off()
                            time.sleep(timer1)
                            
                    elif inst['inst'][0]=='POWDER':
                        print(inst)
                        str1=inst['INOUT'][0]
                        print(str1)
                        if str1=='0':
                            led_pin[1].off()
                            time.sleep(timer1)
                        elif str1=='1':
                            led_pin[1].on()
                            time.sleep(timer1)
                            
                    elif inst['inst'][0]=='TURN':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                        if op['CW']=='0':
                            led_pin[2].on()
                            time.sleep(timer1)
                            led_pin[3].off()
                            time.sleep(timer1)
                            
                            if op['SPEED']=='1':
                                led_pin[4].off()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].off()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='2':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].off()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].off()
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='3':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)

                        if op['CW']=='1':
                            led_pin[2].off()
                            time.sleep(timer1)
                            led_pin[3].on()
                            time.sleep(timer1)
                            
                            if op['SPEED']=='1':
                                led_pin[4].off()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].off()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='2':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].off()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].off()
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='3':
                                led_pin[4].on()
                                time.sleep(timer1)
                                led_pin[5].on()
                                time.sleep(timer1)
                                led_pin[6].on()
                                time.sleep(timer1)
                                led_pin[7].on()
                                time.sleep(timer1)
                                
                    elif inst['inst'][0]=='CIRCLE':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                        
                        led_pin[2].off()
                        led_pin[3].off()

                        if op['SIZE']=='0':
                            if op['CW']=='0':
                                led_pin[4].off()
                                led_pin[5].off()
                                led_pin[6].on()
                                led_pin[7].off()
                            
                            elif op['CW']=='1':
                                led_pin[4].on()
                                led_pin[5].off()
                                led_pin[6].off()
                                led_pin[7].off()

                        elif op['SIZE']=='1':
                                if op['CW']=='0':
                                    led_pin[4].off()
                                    led_pin[5].on()
                                    led_pin[6].on()
                                    led_pin[7].on()
                            
                                elif op['CW']=='1':
                                    led_pin[4].on()
                                    led_pin[5].on()
                                    led_pin[6].off()
                                    led_pin[7].on()
                        
                        elif op['SIZE']=='2':
                            #if op['ptn']=='1':
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
            
                    elif inst['inst'][0]=='CIRCLE3':
                        for key in inst:
                            op[key]=inst[key][0]

                        spi = spidev.SpiDev()
                        spi.open(0, 0)  # SPI0, CE0
                        spi.max_speed_hz = 115200
                        spi.mode = 1  # SPI MODE 1
                        t_size =  int(op['turnsize'])
                        i=0
                        
                        tx_data=[0x00,0x00]
                        print("bb")
                        tx_data[1]=t_size>>8
                        print("aa")
                        tx_data[0]=t_size&0xFF
                        
                        print(tx_data)
                        rx_data=[0xFF,0xFF]
                        error=0
                        led_pin[8].on()
                                               
                        while (tx_data != rx_data):
                            
                            if(i > time_out):
                                error=1
                                break
                            i+=1    
                            tx_data2=tx_data[:]
                            print(f"送信データ: {[f'{b:04X}' for b in tx_data]}")
                            time.sleep(0.1)
                            rx_data = spi.xfer2(tx_data2)    #SPI通信でデータ送信
                            time.sleep(0.1) 
                            rx_data = spi.xfer2([0x00,0x00])   #ダミーデータを送信して、受信データ確認              
                            time.sleep(0.1)
                            print(f"受信データ: {[f'{b:04X}' for b in rx_data]}")
                               
                                
                        led_pin[8].off()
                        spi.close()
                        if(error==1):
                            print("Value setting is incomplete")
                            
                        else:
                            print("Value setting is complete")
                        
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
                    
                    elif inst['inst'][0]=='SLEEP' or inst['inst'][0]=='SLEEP_A':
                        for key in inst:
                            op[key]=inst[key][0]
                        time.sleep(float(op['TIME']))

            else:
                
                inst2[index]=inst
                index=index+1



        except Exception as e:  
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
            print()
            for i in range(n_pin):
                led_pin[i].off()

def run():
    server_address=('localhost',8000)
    server = HTTPServer(server_address, Server_class)
    server.serve_forever()

print('start')

for i in range(n_pin):
    led_pin[i].off()

run()
