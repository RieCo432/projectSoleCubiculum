import math
from datetime import datetime
import time
import color_helper
from circular_list import CircularList


class Room:

    def __init__(self, num_leds, s0, s45, s90, s135, s180, s225, s270, s315, init_philips_hue=False,
                 philips_hue_ip="0.0.0.0", light_names=None):

        # if no light names are specified, replace with empty list
        if light_names is None:
            light_names = []

        # get total number of leds by adding together all edge lengths
        self.num_leds = sum([s0.length, s45.length, s90.length, s135.length, s180.length, s225.length, s270.length,
                             s315.length])

        # try importing the adafruit library and initialize strip. If it fails, demo mode will be used and the strip
        # is just a list of color tuples
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

        # set up philips hue, if fails, features won't be used
        self.phue_setup_done = False
        if init_philips_hue:
            try:
                import phue  # import the python hue library
                try:
                    self.phuebridge = phue.Bridge(philips_hue_ip)  # setup bridge
                    self.phuebridge.connect()  # connect to bridge
                    self.phue_light_names = []  # store all found lights
                    all_lights = self.phuebridge.get_light_objects()  # retrieve all light objects from bridge
                    # cycle through all lights, check if light name in list supplied to init function, then remove from
                    # user supplied list and append to list from above
                    for light in all_lights:
                        if light.name in light_names:
                            light_names.remove(light.name)
                            self.phue_light_names.append(light.name)
                    # if all lights were found, phue_setup_done set to true
                    if len(light_names) == 0:
                        self.phue_setup_done = True
                except phue.PhueRegistrationException:
                    print("Registration Error, link button not pressed in the past 30 seconds")
                    pass
                except phue.PhueRequestTimeout:
                    print("Connection error")
                    pass
            except ImportError:
                print("Error importing phue")
                pass

        # initialize list containing all color values
        self.colors = []
        for i in range(self.num_leds):
            self.colors.append((0, 0, 0))

        # associate supplied edges with correct attributes
        self.north = s0
        self.north_east = s45
        self.east = s90
        self.south_east = s135
        self.south = s180
        self.south_west = s225
        self.west = s270
        self.north_west = s315

        # initialize empty lists for various sets
        self.all_edges_in_order = None
        self.ceiling_edges_clockwise = None
        self.vertical_edges_up = None

    def set_sequences(self, a1, a2, a3, a4, a5, a6, a7, a8, c1, c2, c3, c4, v1, v2, v3, v4):
        # create circular lists for each set with corresponding edges
        self.all_edges_in_order = CircularList((a1, a2, a3, a4, a5, a6, a7, a8))
        self.ceiling_edges_clockwise = CircularList((c1, c2, c3, c4))
        self.vertical_edges_up = CircularList((v1, v2, v3, v4))

    def allocate_leds(self):
        # count up to number of LEDs and assign the number to the correct edges
        # p.ex. number 0 is supplied to first edge in the list, it will count from 0 to whatever its length is, then
        # return that number to be used as first for the next edge
        first = 0
        for edge in self.all_edges_in_order:
            first = edge.allocate_leds(first)

    # effects go here

    # turns all LEDs off
    def leds_off(self):
        # fill the strip with black and update LEDs
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
    # brightness will be increased by some amount per second until final brightness is reached
    # this will take 4 seconds to increase from 0 to 100% at 25% per second
    def increase_brightness(self, final_brightness=1.0, percent_per_second=0.40):
        if not self.demo:
            stamp = datetime.now()
            while True:
                elapsed = (datetime.now() - stamp).total_seconds()
                stamp = datetime.now()
                bri_increase = percent_per_second * elapsed  # brightness increase step is dependant on time elapsed
                # since last cycle
                bri = self.get_brightness()  # obtain current brightness
                # set brightness to lowest value of either 1.0, final brightness or current brightness + increase
                self.set_brightness(min(bri + bri_increase, final_brightness, 1.0))
                # once the brightness reaches the final brightness, the loop will break
                if bri >= final_brightness:
                    break

    # gradually decrease brightness
    # brightness will be decreased by some amount per second until final brightness is reached
    # this will take 4 seconds to decrease from 100% to 0% at 25% per second
    def decrease_brightness(self, final_brightness=0.0, percent_per_second=0.40):
        if not self.demo:
            stamp = datetime.now()
            while True:
                elapsed = (datetime.now() - stamp).total_seconds()
                stamp = datetime.now()
                bri_decrease = percent_per_second * elapsed  # brightness decrease step is dependant on time elapsed
                # since last cycle
                bri = self.get_brightness()  # obtain current brightness
                # set brightness to highest value of either 0, final brightness or current brightness - increase
                self.set_brightness(max(bri - bri_decrease, final_brightness, 0.0))
                # once the brightness reaches the final brightness, the loop will break
                if bri <= final_brightness:
                    break

    def get_brightness(self):
        # find brightness by finding the absolute highest value for r, g, b in the strip, then divide the highest by 255
        r = 0
        g = 0
        b = 0
        for led in self.leds:
            r = max(r, led[0])
            g = max(g, led[1])
            b = max(b, led[2])
        brightest = max(r, g, b) / 255

        return brightest

    def set_brightness(self, final_brightness):
        brightness = self.get_brightness()  # store current brightness
        if brightness == 0:  # avoid division by 0 error
            brightness = 0.001
        for led_index in range(len(self.leds)):  # for each led
            # find r, g, b values
            r = self.leds[led_index][0]
            g = self.leds[led_index][1]
            b = self.leds[led_index][2]

            # new r, g, b values will be ratio of desired brightness by current brightness, times original value
            new_r = final_brightness / brightness * r
            new_g = final_brightness / brightness * g
            new_b = final_brightness / brightness * b

            # build color tuple, limit to 255 and convert to int
            color_int = (min(int(new_r), 255), min(int(new_g), 255), min(int(new_b), 255))
            self.leds[led_index] = color_int  # set color

        if not self.demo:
            self.leds.show()

    # build a list of lists of LEDs, enabling horizontal circular effect with or without vertical elements
    def build_list_horizontal_circle(self, include_vertical=True):
        list_of_leds = CircularList()

        if include_vertical:
            # iterate through all edges in order and add LED numbers of ceiling strips to list, add list of LEDs in
            # vertical edges as list so they function as a single LED
            for edge in self.all_edges_in_order:
                if edge in self.ceiling_edges_clockwise:
                    for led in edge.leds:
                        list_of_leds.append([led])
                else:
                    list_of_leds.append(edge.leds)
        else:
            # iterate through edges and add the led numbers to the circular list
            for edge in self.ceiling_edges_clockwise:
                for led in edge.leds:
                    list_of_leds.append([led])

        return list_of_leds

    # build a list of lists of LEDs, enabling vertical upwards effect with or without horizontal elements
    def build_list_vertical_straight(self, include_horizontal = True):
        list_of_leds = CircularList()

        for i in range(0, self.vertical_edges_up[0].length):
            list_of_leds.append([self.vertical_edges_up[0].leds[i], self.vertical_edges_up[1].leds[i],
                                 self.vertical_edges_up[2].leds[i], self.vertical_edges_up[3].leds[i]])

        if include_horizontal:
            all_horizontal = []
            for edge in self.ceiling_edges_clockwise:
                for n in edge.leds:
                    all_horizontal.append(n)

            list_of_leds.append(all_horizontal)

        return list_of_leds

    # start is the index where the starting hue is applied
    # end is the index where starting hue completes a cycle
    # cycles determines how many full rotations are done (for less than full rotation use 0)
    # speed is how quickly the starting hue moves around in steps per second (1 step = 1 LED)
    # starting hue determines which color is used at the main point, hue is in degrees (0 is red, 120 is green,
    # 240 is green)
    def rainbow(self, list_of_leds, start_index=None, end_index=None, cycles=0, speed=10, starting_hue=0.0):
        # initialize a circular list to store led numbers that are involved

        # if no starting point is given, select first led of first ceiling edge
        if speed >= 0:
            if start_index is None:
                start_index = 0
            if end_index is None:
                end_index = -1

        elif speed < 0:
            if start_index is None:
                start_index = -1
            if end_index is None:
                end_index = 0

        start = list_of_leds[start_index]
        end = list_of_leds[end_index]

        # find index of starting led in list and shift backwards so starting LED is at the beginning
        list_of_leds.shiftBackwardN(start_index)

        # determine how much the hue needs to increase per LED/step
        hue_increase_per_step = 360.0 / len(list_of_leds)

        # initialize loop and counter variables
        cycle = 0
        stop = False
        stamp = datetime.now()
        theoretical_movement = 0
        first_iter = True
        rest = 0
        while not stop:
            # move animation if needed
            actual_movement = 0
            theoretical_movement = speed * (datetime.now() - stamp).total_seconds()
            if theoretical_movement + rest >= 1:
                actual_movement = int(math.floor(theoretical_movement + rest))
                rest = theoretical_movement - actual_movement
                list_of_leds.shiftBackwardN(actual_movement)
            elif theoretical_movement - rest <= -1:
                actual_movement = - int(math.ceil(theoretical_movement - rest))
                rest = theoretical_movement - actual_movement
                list_of_leds.shiftForwardN(actual_movement)

            if actual_movement != 0 or first_iter:
                if first_iter:
                    first_iter = False

                hue = starting_hue  # reset hue to starting hue
                # for each entry in list, check if entry is a list
                # if yes, set color to current hue for every LED number in list
                # if not, set color of the specific LED to current hue
                #
                # then increase hue and modulo 360 it
                for step in list_of_leds:
                    for led_num in step:
                        self.leds[led_num] = color_helper.hue_to_rgb(math.floor(hue))
                    hue += hue_increase_per_step
                    hue %= 360

                # update physical LEDs
                stamp = datetime.now()
                if not self.demo:
                    self.leds.show()
                else:
                    print(datetime.now(), list_of_leds._data)

                if actual_movement >= 1:
                    # if endpoint LED is inside next movement and desired number of cycles has been reached, stop loop
                    if end in list_of_leds[0:actual_movement + 1] and cycle == cycles:
                        stop = True

                    # if endpoint LED is inside next movement, but number of cycles has not been reached yet,
                    # increase cycle
                    # counter
                    if end in list_of_leds[0:actual_movement + 1]:
                        cycle += 1
                elif actual_movement <= -1:
                    # if endpoint LED is inside next movement and desired number of cycles has been reached, stop loop
                    if end in list_of_leds[-actual_movement:0] and cycle == cycles:
                        stop = True

                    # if endpoint LED is inside next movement, but number of cycles has not been reached yet,
                    # increase cycle
                    # counter
                    if end in list_of_leds[-actual_movement:0]:
                        cycle += 1



