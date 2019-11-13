from room import Room
from edge import Edge
from Compass import DataFlow, Direction
from config import build_living_room

living_room = build_living_room()

living_room.hue_off()
living_room.rainbow_ceiling_only(speed=10, include_vertical=True)
living_room.leds_off()
living_room.hue_on()
