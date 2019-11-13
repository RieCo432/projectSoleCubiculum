from room import Room
from edge import Edge
from Compass import DataFlow, Direction
import time
from config import build_living_room

living_room = build_living_room()

living_room.hue_off()
time.sleep(2)
living_room.rainbow_ceiling_only(speed=60, include_vertical=True)
time.sleep(1)
living_room.leds_off()
time.sleep(1)
living_room.hue_on()
