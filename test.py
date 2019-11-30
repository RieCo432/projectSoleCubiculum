from room import Room
from edge import Edge
from Compass import DataFlow, Direction
import time
from config import build_living_room

living_room = build_living_room()

living_room.hue_off()
time.sleep(2)
if living_room.demo:
    mult = 5
else:
    mult = 1
living_room.hue_span_color_cylce(living_room.build_list_horizontal_circle(), compress=16,speed=15 * mult)
time.sleep(2)
living_room.hue_span_color_cylce(living_room.build_list_vertical_straight(), compress=4, speed=3 * mult)
living_room.decrease_brightness(percent_per_second=0.25)
living_room.leds_off()
time.sleep(1)
living_room.hue_on()
