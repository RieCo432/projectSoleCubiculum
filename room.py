import math
from datetime import datetime
import time
import color_helper
from circular_list import CircularList

class Room:

    def __init__(self, num_leds, s0, s45, s90, s135, s180, s225, s270, s315, init_philips_hue=False,
                 philips_hue_IP="0.0.0.0", light_names=[]):

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

        # set up philips hue
        self.phue_setup_done = False
        try:
            import phue
            try:
                self.phuebridge = phue.Bridge(philips_hue_IP)
                self.phuebridge.connect()
                self.phue_light_names = []
                all_lights = self.phuebridge.get_light_objects()
                for light in all_lights:
                    if light.name in light_names:
                        light_names.remove(light.name)
                        self.phue_light_names.append(light.name)
                if len(light_names) == 0:
                    self.phue_setup_done = True
            except phue.PhueRegistrationException:
                print("Registration Error, link button not pressed in the past 30 seconds")
        except ImportError:
            print("Error importing phue")


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

    # turns all LEDs off
    def leds_off(self):
        if not self.demo:
            self.leds.fill((0, 0, 0))
            self.leds.show()

    # turn off hue lights
    def hue_off(self):
        if self.phue_setup_done:
            self.phuebridge.set_light(self.phue_light_names, "on", False)

    # turn on hue lights
    def hue_on(self):
        if self.phue_setup_done:
            self.phuebridge.set_light(self.phue_light_names, "on", True)

    # gradually increase brightness
    def increase_brightness(self, final_brightness=1.0, percent_per_second=0.40):
        if not self.demo:
            stamp = datetime.now()
            while True:
                elapsed = (datetime.now() - stamp).total_seconds()
                bri_increase = percent_per_second * elapsed
                bri = self.leds.brightness()
                self.leds.brightness(min(bri + bri_increase, final_brightness, 1.0))
                self.leds.show()
                if bri >= final_brightness:
                    break

    # gradually decrease brightness
    def decrease_brightness(self, final_brightness=0.0, percent_per_second=0.40):
        if not self.demo:
            stamp = datetime.now()
            while True:
                elapsed = (datetime.now() - stamp).total_seconds()
                bri_decrease = percent_per_second * elapsed
                bri = self.leds.brightness()
                self.leds.brightness(max(bri + bri_decrease, final_brightness, 0.0))
                self.leds.show()
                if bri <= final_brightness:
                    break

    # start is number of LED where the starting hue is applied
    # end is number of LED where starting hue needs to go to
    # cycles determines how many full rotations are done (for less than full rotation use 0)
    # speed is how quickly the starting hue moves around in LEDs per second
    # starting hue determines which color is used at the main point, hue is in degrees (0 is red, 120 is green,
    # 240 is green)
    def rainbow_ceiling_only(self, start=None, end=None, cycles=0, speed=10, starting_hue=0.0, include_vertical=False):
        # initialize a circular list to store led numbers that are involved
        list_of_leds = CircularList()

        # if no starting point is given, select first led of first ceiling edge
        if start is None:
            start = self.ceiling_edges_clockwise[0].leds[0]
        # if no end is given, select last led of last ceiling edge
        if end is None:
            end = self.ceiling_edges_clockwise[-1].leds[-1]
        if include_vertical:
            # iterate through all edges in order and add LED numbers of ceiling strips to list, add list of LEDs in
            # vertical edges as list so they function as a single LED
            for edge in self.all_edges_in_order:
                if edge in self.ceiling_edges_clockwise:
                    for led in edge.leds:
                        list_of_leds.append(led)
                else:
                    list_of_leds.append(edge.leds)
        else:
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
        stamp = datetime.now()
        while not stop:
            # if no timestamp is set, or enough time has elapsed, update lighting
            if True: # stamp is None or (datetime.now() - stamp).total_seconds() >= 1.0 / speed:
                hue = starting_hue  # reset hue to starting hue
                # for each entry in list, check if entry is a list
                # if yes, set color to current hue for every LED nunber in list
                # if not, set color of the specific LED to current hue
                #
                # then increase hue and modulo 360 it
                for entry in list_of_leds:
                    if type(entry) == type(list()):
                        for led_num in entry:
                            self.leds[led_num] = color_helper.hue_to_rgb(math.floor(hue))
                    else:
                        self.leds[entry] = color_helper.hue_to_rgb(math.floor(hue))
                    hue += hue_increase_per_led
                    hue %= 360

                # shift LED list backwards if needed
                theoretical_movement = int(math.floor(speed * (datetime.now() - stamp).total_seconds()))
                if theoretical_movement >= 1:
                    list_of_leds.shiftBackwardN(theoretical_movement)
                    stamp = datetime.now()

                # if endpoint LED is inside next movement and desired number of cycles has been reached, stop loop
                if end in list_of_leds[0:theoretical_movement+1] and cycle == cycles:
                    stop = True

                # if endpoint LED is inside next movement, but number of cycles has not been reached yet, increase cycle
                # counter
                if end in list_of_leds[0:theoretical_movement+1]:
                    cycle += 1

                # update physical LEDs and record new timestamp
                if not self.demo:
                    self.leds.show()
                else:
                    pass
                    print(list_of_leds._data)
                    # time.sleep(0.02)



