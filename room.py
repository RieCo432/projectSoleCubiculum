from datetime import datetime
import time
import color_helper
from circular_list import CircularList


class Room:

    def __init__(self, num_leds, s0, s45, s90, s135, s180, s225, s270, s315):

        self.num_leds = sum([s0.length, s45.length, s90.length, s135.length, s180.length, s225.length, s270.length,
                             s315.length])

        try:
            import adafruit_ws2801 as af
            import board
            self.demo = False
            self.leds = af.WS2801(board.SCK, board.MOSI, self.num_leds, auto_write=False)
        except ImportError:
            print("running in demo mode")
            time.sleep(3)
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

    # effects go here

    # start is number of LED where the starting hue is applied
    # end is number of LED where starting hue needs to go to
    # cycles determines how many full rotations are done (for less than full rotation use 0)
    # speed is how quickly the starting hue moves around in LEDs per second
    # starting hue determines which color is used at the main point, hue is in degrees (0 is red, 120 is green,
    # 240 is green)
    def rainbow_ceiling_only(self, start=None, end=None, cycles=0, speed=10, starting_hue=0.0):
        # initialize a circular list to store led numbers that are involved
        list_of_leds = CircularList()

        # if no starting point is given, select first led of first ceiling edge
        if start is None:
            start = self.ceiling_edges_clockwise[0].leds[0]
        # if no end is given, select last led of last ceiling edge
        if end is None:
            end = self.ceiling_edges_clockwise[-1].leds[-1]
        # iterate through edges and add the led numbers to the circular list
        for edge in self.ceiling_edges_clockwise:
            for led in edge.leds:
                list_of_leds.append(led)

        # find index of starting led in list and shift backwards so starting LED is at the beginning
        shift_amount = list_of_leds.index(start)
        list_of_leds.shiftBackwardN(shift_amount)

        # determine how much the hue needs to increase per LED/step
        hue_increase_per_led = 360.0 / len(list_of_leds)

        # initialize loop and counter variables
        cycle = 0
        stop = False
        stamp = None
        while not stop:
            # if no timestamp is set, or enough time has elapsed, update lighting
            if stamp is None or (datetime.now() - stamp).total_seconds() >= 1.0 / speed:
                hue = starting_hue  # reset hue to starting hue
                # for each LED number in list, set color to current hue, increase hue and modulo 360 it
                for led_num in list_of_leds:
                    self.leds[led_num] = color_helper.hue_to_rgb(hue)
                    hue += hue_increase_per_led
                    hue %= 360
                # if the first LED in the list is the endpoint and desired number of cycles has been reached, stop loop
                if list_of_leds[0] == end and cycle == cycles:
                    stop = True
                # if first LED in list is endpoint, but number of cycles has not been reached yet, increase cycle
                # counter
                if list_of_leds[0] == end:
                    cycle += 1
                # shift LED list back wards by one
                list_of_leds.shiftBackward()
                # update physical LEDs and record new timestamp
                if not self.demo:
                    self.leds.show()
                else:
                    print(self.leds)
                stamp = datetime.now()



