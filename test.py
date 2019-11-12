from room import Room
from edge import Edge
from Compass import DataFlow, Direction
from config import build_living_room

living_room = build_living_room()

l = []
for edge in living_room.all_edges_in_order:
    for i in edge.leds:
        l.append(i)

print(l)
