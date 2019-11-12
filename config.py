from room import Room
from Compass import DataFlow, Direction
from edge import Edge


def build_living_room():

    living_room = Room()

    living_room.north = Edge(living_room.horizontal_length_long, Direction.N, DataFlow.W_TO_E)
    living_room.east = Edge(living_room.horizontal_length_short, Direction.E, DataFlow.N_TO_S)
    living_room.south = Edge(living_room.horizontal_length_long, Direction.S, DataFlow.E_TO_W)
    living_room.west = Edge(living_room.horizontal_length_short, Direction.W, DataFlow.S_TO_N)

    living_room.north_east = Edge(living_room.vertical_length, Direction.NE, DataFlow.FLOOR_TO_CEIL)
    living_room.south_east = Edge(living_room.vertical_length, Direction.SE, DataFlow.FLOOR_TO_CEIL)
    living_room.south_west = Edge(living_room.vertical_length, Direction.SW, DataFlow.FLOOR_TO_CEIL)
    living_room.north_west = Edge(living_room.vertical_length, Direction.NW, DataFlow.FLOOR_TO_CEIL)

    living_room.all_edges_in_order = [living_room.south_east, living_room.south, living_room.south_west, living_room.west, living_room.north_west, living_room.north, living_room.north_east, living_room.east]

    return living_room