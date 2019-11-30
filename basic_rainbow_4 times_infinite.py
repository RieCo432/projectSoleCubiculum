import time
from config import build_living_room

living_room = build_living_room()
time.sleep(2)
while True:
    living_room.hue_span_color_cylce(living_room.build_list_horizontal_circle(), compress=4, speed=30, cycles=1000)
