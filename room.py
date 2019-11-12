from circular_list import CircularList
from edge import Edge
from Compass import DataFlow, Direction

class Room:

    def __init__(self, num_leds, s0, s45, s90, s135, s180, s225, s270, s315):

        self.num_leds = sum([s0.length, s45.length, s90.length, s135.length, s180.length, s225.length, s270.length,
                             s315.length])

        try:
            import Adafruit_WS2801 as af
            import board
            self.demo = False
            self.leds = af.WS2801(board.SCK, board.MOSI, self.num_leds, auto_write=False)
        except ImportError:
            self.demo = True
            self.leds = [(0, 0, 0)] * self.num_leds

        self.colors = []
        for i in range(self.num_leds):
            self.colors.append((0, 0, 0))
        self.master_brightness = 1.0

        # empty lists for walls
        self.north = s0
        self.north_east = s45
        self.east = s90
        self.south_east = s135
        self.south = s180
        self.south_west = s225
        self.west = s270
        self.north_west = s315

        self.all_edges_in_order = None
        self.ceiling_edges_clockwise = None
        self.vertical_edges_up = None
        self.ceiling_edges_counterclockwise = None
        self.vertical_edges_down = None

    def set_sequences(self, a1, a2, a3, a4, a5, a6, a7, a8, c1, c2, c3, c4, v1, v2, v3, v4):
        self.all_edges_in_order = CircularList((a1, a2, a3, a4, a5, a6, a7, a8))
        self.ceiling_edges_clockwise = CircularList((c1, c2, c3, c4))
        self.vertical_edges_up = CircularList((v1, v2, v3, v4))
        self.ceiling_edges_counterclockwise = self.ceiling_edges_clockwise[::-1]
        self.vertical_edges_down = self.vertical_edges_up[::-1]

    def allocate_leds(self):

        first = 0
        for edge in self.all_edges_in_order:
            first = edge.allocate_leds(first)

        print(self.all_edges_in_order)
