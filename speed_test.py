import adafruit_ws2801 as af
import board
import time
from datetime import datetime

print("number of leds: ")
n = int(input())

leds = af.WS2801(board.SCK, board.MOSI, n, auto_write=False)

leds.fill((0,0,0))
leds.show()
time.sleep(1)
stamp = datetime.now()

for i in range(len(leds)):
    leds.fill((0,0,0))
    leds[i] = (255,255,255)
    leds.show()

total_time = (datetime.now() - stamp).total_seconds()
print("total time:", total_time)
