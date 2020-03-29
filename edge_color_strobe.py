import time
from config import build_living_room
from random import randint


living_room = build_living_room()
time.sleep(2)
colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,255)]
while True:
    edge_num = randint(0, len(living_room.all_edges_in_order)-1)
    for i in range(len(living_room.all_edges_in_order)):
        if i == edge_num:
            color = colors[randint(0, len(colors)-1)]
        else:
            color = (0,0,0)
        for led_num in living_room.all_edges_in_order[i].leds:
            living_room.set_led(led_num, color)

    living_room.update()
