#!/usr/bin/env python3

from shelf_functions import board_positions, union, fit_to_size

# ++++++++++++++++ setup [millimeters}
THICKNESS = 20
WIDTH = 2500
HEIGHT = 2500
DEPTH = 400
DEPTH_EXTRA = 500
# ++++++++++++++++

# set compartment heights
compartment_heights = [350, 500, 300, 250, 800]

fit_to_size(compartment_heights, THICKNESS, HEIGHT)

# print(compartment_heights)

# example_compartments = [200, 100, 50]
compartment_widths = [[100, 200, 300, 400], [110, 220, 330, 440], [111, 222, 333, 444], [321, 210, 120]]
# compartment_widths = [example_compartments] * len(compartment_heights)

# print(compartment_widths)

all_compartments = []

for i in range(len(compartment_widths)):
	fitted = compartment_widths[i] + fit_to_size(compartment_widths[i], THICKNESS, WIDTH)
	all_compartments += [fitted]

print(all_compartments)


# vertical_coordinates = board_positions(compartment_widths, THICKNESS, HEIGHT)
# print(vertical_coordinates)