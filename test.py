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
living_room.hue_span_color_cylce(living_room.build_list_horizontal_circle(), starting_hue=0, ending_hue=120, speed=10 * mult)
time.sleep(2)
living_room.hue_span_color_cylce(living_room.build_list_vertical_straight(), starting_hue=120, ending_hue=240,  speed=2 * mult)
living_room.decrease_brightness(percent_per_second=0.25)
living_room.leds_off()
time.sleep(1)
living_room.hue_on()
