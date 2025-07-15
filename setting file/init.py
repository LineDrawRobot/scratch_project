
from gpiozero import LED
from time import sleep

# Raspberry Pi の BCM 番号で使われるすべての GPIO（使用中のピンだけでも可）
gpio_pins = [5,6,13,19,26,16,20,21,25] 

leds = [LED(pin) for pin in gpio_pins]

# すべてOFFにする
for led in leds:
    led.off()

print("すべてのGPIOをLOWに設定しました。")
