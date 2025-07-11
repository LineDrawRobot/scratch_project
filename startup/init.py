
from gpiozero import LED
from time import sleep

# Raspberry Pi の BCM 番号で使われるすべての GPIO（使用中のピンだけでも可）
gpio_pins = [
    2, 3, 4, 5, 6, 9, 10, 11,
    12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24, 25, 26, 27
]

leds = [LED(pin) for pin in gpio_pins]

# すべてOFFにする
for led in leds:
    led.off()

print("すべてのGPIOをLOWに設定しました。")
