import spidev
import time
import random

spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0, CE0
spi.max_speed_hz = 115200
spi.mode = 1  # SPI MODE 0

print("=== SPI 通信テスト開始 ===")
n=0
n1=0
n2=0
miss=0
x=0

try:
    while True:
        #aa
        tx_data = [0x00,0x00]
        tx_data[0]=tx_data[0]+n1
        tx_data[1]=tx_data[1]+n2
        tx_data2=tx_data[:]
        # 2バイト送信＆同時に2バイト受信
 
        rx_data=spi.xfer2(tx_data2)
        time.sleep(0.1)
        rx_data=spi.xfer2([0xFF,0xFE])
        time.sleep(0.1)
        #rx_data3=spi.xfer2([0xAA,0xBB])
        #time.sleep(0.1)
        #print(f"送信データ: {[f'{b:04X}' for b in tx_data]}")
        #print(f"受信データ: {[f'{b:04X}' for b in rx_data]}")
        #print(f"受信データ: {[f'{b:04X}' for b in rx_data2]}")
        #print(f"受信データ: {[f'{b:04X}' for b in rx_data3]}")
        if(tx_data==rx_data):
            print(f"送信データ: {[f'{b:04X}' for b in tx_data]}")
            print(f"受信データ: {[f'{b:04X}' for b in rx_data]}")
            #print(n1)
            #print(n2)
            n1=random.randint(0,255)
            n2=random.randint(0,254)
            n+=1
            print(n)
            print(miss)
        else:
            miss+=1
            #print(n)
            #print(miss)
        #time.sleep(1)
except KeyboardInterrupt:
    print("\n終了します")
    spi.close()
