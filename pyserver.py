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
import RPi.GPIO as GPIO
import sys
import spidev


count = 0


volume=0
b=1
G=0
data=0

led_pin=[14,15,18,23,24,25,12,7,26] #SPI実装にGPIO8をGPIO12に変更
str1='0'
op = {'inst': '0','ForB': '0','SPEED': '0','CW':'0','ptn':'0','SIZE':'0'}
timer1=0
index =0

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)

def parse(path):
    
    qs = p.urlparse(path).query
    qs_d = p.parse_qs(qs)
    return qs_d

class Server_class(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            global op
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            inst=parse(self.path)
            if inst['inst'][0]=='RESET':
                index=0;
            elif inst['inst'][0]=='EXECUTE':
                for i in range(0,index):
                    inst = inst2[i]

                    if inst['inst'][0]=='START':
                        GPIO.output(led_pin[0],GPIO.HIGH)
                        print('START')
                    
                    elif inst['inst'][0]=='STOP':
                        for i in range(8):
                            GPIO.output(led_pin[i],GPIO.LOW)                  
                    print('STOP')
                    

                    elif inst['inst'][0]=='TIREON':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                        if op['ForB']=='1':
                            GPIO.output(led_pin[2],GPIO.HIGH)
                            time.sleep(timer1)
                            GPIO.output(led_pin[3],GPIO.HIGH)
                            time.sleep(timer1)
                                    
                            if op['SPEED']=='1':
                                GPIO.output(led_pin[4],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)
                                    
                            elif op['SPEED']=='2':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.LOW)
                                time.sleep(timer1)

                            elif op['SPEED']=='3':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)
                            
                        elif op['ForB']=='0':
                            GPIO.output(led_pin[2],GPIO.LOW)
                            time.sleep(timer1)
                            GPIO.output(led_pin[3],GPIO.LOW)
                            time.sleep(timer1)
                                    
                            if op['SPEED']=='1':
                                GPIO.output(led_pin[4],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)
                                    
                            elif op['SPEED']=='2':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.LOW)
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='3':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)

                    elif inst['inst'][0]=='TIREOFF':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                            
                        for i in range(2,8):
                            GPIO.output(led_pin[i],GPIO.LOW)
                            time.sleep(timer1)
                            
                    elif inst['inst'][0]=='POWDER':
                        print(inst)
                        str1=inst['INOUT'][0]
                        print(str1)
                        if str1=='0':
                            GPIO.output(led_pin[1],GPIO.LOW)
                            time.sleep(timer1)
                        elif str1=='1':
                            GPIO.output(led_pin[1],GPIO.HIGH)
                            time.sleep(timer1)
                            
                    elif inst['inst'][0]=='TURN':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                        if op['CW']=='0':
                            GPIO.output(led_pin[2],GPIO.HIGH)
                            time.sleep(timer1)
                            GPIO.output(led_pin[3],GPIO.LOW)
                            time.sleep(timer1)
                            
                            if op['SPEED']=='1':
                                GPIO.output(led_pin[4],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='2':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.LOW)
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='3':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)

                        if op['CW']=='1':
                            GPIO.output(led_pin[2],GPIO.LOW)
                            time.sleep(timer1)
                            GPIO.output(led_pin[3],GPIO.HIGH)
                            time.sleep(timer1)
                            
                            if op['SPEED']=='1':
                                GPIO.output(led_pin[4],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='2':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.LOW)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.LOW)
                                time.sleep(timer1)
                                
                            elif op['SPEED']=='3':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                time.sleep(timer1)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                time.sleep(timer1)
                                
                    elif inst['inst'][0]=='CIRCLE':
                        for key in inst:
                            op[key]=inst[key][0]
                        print(op)
                        
                        GPIO.output(led_pin[2],GPIO.LOW)
                        GPIO.output(led_pin[3],GPIO.LOW)

                        if op['SIZE']=='0':
                            if op['CW']=='0':
                                GPIO.output(led_pin[4],GPIO.LOW)
                                GPIO.output(led_pin[5],GPIO.LOW)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                GPIO.output(led_pin[7],GPIO.LOW)
                            
                            elif op['CW']=='1':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                GPIO.output(led_pin[5],GPIO.LOW)
                                GPIO.output(led_pin[6],GPIO.LOW)
                                GPIO.output(led_pin[7],GPIO.LOW)

                        elif op['SIZE']=='1':
                                if op['CW']=='0':
                                    GPIO.output(led_pin[4],GPIO.LOW)
                                    GPIO.output(led_pin[5],GPIO.HIGH)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.HIGH)
                            
                                elif op['CW']=='1':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.HIGH)
                                    GPIO.output(led_pin[6],GPIO.LOW)
                                    GPIO.output(led_pin[7],GPIO.HIGH)
                        
                        elif op['SIZE']=='2':
                            #if op['ptn']=='1':
                            if op['CW']=='0':
                                GPIO.output(led_pin[4],GPIO.LOW)
                                GPIO.output(led_pin[5],GPIO.HIGH)
                                GPIO.output(led_pin[6],GPIO.HIGH)
                                GPIO.output(led_pin[7],GPIO.LOW)
                                
                            elif op['CW']=='1':
                                GPIO.output(led_pin[4],GPIO.HIGH)
                                GPIO.output(led_pin[5],GPIO.LOW)
                                GPIO.output(led_pin[6],GPIO.LOW)
                                GPIO.output(led_pin[7],GPIO.HIGH)
                                
                        """ 
                            elif op['ptn']=='2':
                                if op['CW']=='0':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.LOW)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.HIGH)
                                
                                elif op['CW']=='1':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.HIGH)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.LOW)
                        
                        elif op['SIZE']=='3':
                            if op['ptn']=='1':
                                if op['CW']=='0':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.LOW)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.HIGH)
                                
                                elif op['CW']=='1':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.HIGH)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.LOW)
                            
                            elif op['ptn']=='2':
                                if op['CW']=='0':
                                    GPIO.output(led_pin[4],GPIO.LOW)
                                    GPIO.output(led_pin[5],GPIO.HIGH)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.LOW)
                                
                                elif op['CW']=='1':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.LOW)
                                    GPIO.output(led_pin[6],GPIO.LOW)
                                    GPIO.output(led_pin[7],GPIO.HIGH)
                                    """
            
                    elif inst['inst'][0]=='CIRCLE3':
                        for key in inst:
                            op[key]=inst[key][0]
                        CE = 0
                        spi = spidev.SpiDev()
                        spi.open(0, CE)
                        spi.mode = 3
                        spi.max_speed_hz = 115200
                        writeData = 0
                        i=0
                        a=0
                        b=-1
                        
                        GPIO.output(led_pin[8],GPIO.HIGH)

                        
                        while (a!= b):
                            writeData = [int(op['turnsize'])]
                            a=writeData[0]
                            
                            while (a!= b):
                            print("a")
                            #print(i)
                            print(a)
                            writeData[0]=a
                            writeData2=[0]
                            if (a > 255):
                            writeData[0]=writeData[0] % 256
                            writeData2[0]=int(a/256)
                            #writeData=str(writeData)
                            print(writeData)
                            print(writeData2)
                            spi.xfer(writeData2)
                            #print("C")
                            time.sleep(0.1)
                            spi.xfer(writeData)
                            #print("D")
                            time.sleep(0.1)
                            resp = spi.xfer2([0x00,0x00]) 
                            #print("E")
                            resp2 = spi.xfer2([0x00,0x00])                 #SPI通信で値を読み込む
            
                            #print(resp)
                            #print(resp2)
                            #print(resp[1]*256+resp2[0])
                            i+=1
                            b=resp[1]*256+resp2[0]
            
                            time.sleep(0.1)
                        GPIO.output(26,GPIO.LOW)
                        print("c")
                        spi.close()
                        if op['CW']=='0':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.LOW)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.HIGH)
                                
                        elif op['CW']=='1':
                                    GPIO.output(led_pin[4],GPIO.HIGH)
                                    GPIO.output(led_pin[5],GPIO.HIGH)
                                    GPIO.output(led_pin[6],GPIO.HIGH)
                                    GPIO.output(led_pin[7],GPIO.LOW)
                    
                    elif inst['inst'][0]=='SLEEP':
                        for key in inst:
                            op[key]=inst[key][0]
                        time.sleep(int(op['TIME']))

            else:
                inst2[index]=inst



        except Exception as e:  
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
            print()

def run():
    server_address=('localhost',8000)
    server = HTTPServer(server_address, Server_class)
    server.serve_forever()

print('start')
for i in range(8):
    GPIO.output(led_pin[i],GPIO.LOW)
run()
