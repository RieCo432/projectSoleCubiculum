from room import Room
from Compass import DataFlow, Direction
from edge import Edge


def build_living_room():

    living_room = Room()

    living_room.n = Edge(living_room.horizontal_length_long, Direction.N, DataFlow.W_TO_E)
    living_room.e = Edge(living_room.horizontal_length_short, Direction.E, DataFlow.N_TO_S)
    living_room.s = Edge(living_room.horizontal_length_long, Direction.S, DataFlow.E_TO_W)
    living_room.w = Edge(living_room.horizontal_length_short, Direction.W, DataFlow.S_TO_N)

    living_room.ne = Edge(living_room.vertical_length, Direction.NE, DataFlow.FLOOR_TO_CEIL)
    living_room.se = Edge(living_room.vertical_length, Direction.SE, DataFlow.FLOOR_TO_CEIL)
    living_room.sw = Edge(living_room.vertical_length, Direction.SW, DataFlow.FLOOR_TO_CEIL)
    living_room.nw = Edge(living_room.vertical_length, Direction.NW, DataFlow.FLOOR_TO_CEIL)

    living_room.all_edges_in_order = [living_room.se, living_room.s, living_room.sw, living_room.w, living_room.nw, living_room.n, living_room.ne, living_room.e]

    return living_room