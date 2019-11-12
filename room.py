from edge import Edge
from Compass import DataFlow, Direction

class Room:

    def __init__(self, ):
        # LEDs per strip
        self.vertical_length = 69
        self.horizontal_length_short = 108
        self.horizontal_length_long = 149

        # empty lists for walls
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.north_east = None
        self.south_east = None
        self.south_west = None
        self.north_west = None

        self.all_edges_in_order = []

    def allocate_leds(self):

        first = 0
        for edge in self.all_edges_in_order:
            first = edge.allocate_leds(first)

        print(self.all_edges_in_order)

