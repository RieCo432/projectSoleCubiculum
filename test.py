from room import Room
from edge import Edge
from Compass import DataFlow, Direction
import time
from config import build_living_room

living_room = build_living_room()

living_room.hue_off()
time.sleep(2)
living_room.rainbow(living_room.build_list_horizontal_circle(), speed=10)
time.sleep(2)
living_room.rainbow(living_room.build_list_vertical_straight(), speed=2)
living_room.decrease_brightness(percent_per_second=0.25)
living_room.leds_off()
time.sleep(1)
living_room.hue_on()
