import Adafruit_WS2801 as af
import Adafruit_GPIO.SPI as SPI
import time
from datetime import datetime
import RPi.GPIO as GPIO

SPI_PORT = 0
SPI_DEVICE = 0

print("number of leds: ")
n = int(input())

leds = af.WS2801Pixels(n, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

leds.clear()
leds.show()
time.sleep(1)
stamp = datetime.now()

for i in range(leds.count()):
    leds.clear()
    leds.set_pixel(i, af.RGB_to_color(255,255,255))
    leds.show()

total_time = (datetime.now() - stamp).total_seconds()
print("total time:", total_time)
