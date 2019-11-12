from edge import Edge
from Compass import DataFlow, Direction

class Room:

    def __init__(self, ):
        # LEDs per strip
        self.vertical_length = 69
        self.horizontal_length_short = 108
        self.horizontal_length_long = 149

        # empty lists for walls
        self.n = None
        self.e = None
        self.s = None
        self.w = None
        self.ne = None
        self.se = None
        self.sw = None
        self.nw = None

        self.all_edges_in_order = []

    def allocate_leds(self):

        first = 0
        for edge in self.all_edges_in_order:
            first = edge.allocate_leds(first)

        print(self.all_edges_in_order)

