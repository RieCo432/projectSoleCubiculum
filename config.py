from circular_list import CircularList
from room import Room
from Compass import DataFlow, Direction
from edge import Edge


def build_living_room():

    living_room = Room()

    vertical_length = 69
    horizontal_length_short = 108
    horizontal_length_long = 149

    living_room.north = Edge(horizontal_length_long, Direction.N, DataFlow.W_TO_E)
    living_room.east = Edge(horizontal_length_short, Direction.E, DataFlow.N_TO_S)
    living_room.south = Edge(horizontal_length_long, Direction.S, DataFlow.E_TO_W)
    living_room.west = Edge(horizontal_length_short, Direction.W, DataFlow.S_TO_N)

    living_room.north_east = Edge(vertical_length, Direction.NE, DataFlow.FLOOR_TO_CEIL)
    living_room.south_east = Edge(vertical_length, Direction.SE, DataFlow.FLOOR_TO_CEIL)
    living_room.south_west = Edge(vertical_length, Direction.SW, DataFlow.FLOOR_TO_CEIL)
    living_room.north_west = Edge(vertical_length, Direction.NW, DataFlow.FLOOR_TO_CEIL)

    living_room.set_sequences(living_room.north_east, living_room.north, living_room.north_west, living_room.west,
                              living_room.south_west, living_room.south, living_room.south_east, living_room.east,
                              living_room.north, living_room.west, living_room.south, living_room.east,
                              living_room.north_east, living_room.north_west, living_room.south_west,
                              living_room.south_east)

    living_room.allocate_leds()



    return living_room
