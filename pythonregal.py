#!/usr/bin/env python3

import random
import numpy as np

from shelf_functions import union, fit_to_size

# ++++++++++++++++ setup [millimeters}
THICKNESS = 20
WIDTH = 2500
HEIGHT = 2500
DEPTH = 400
DEPTH_EXTRA = 500
# ++++++++++++++++

# lists:
# heights
# widths
# horizontal boards
# vertical boards

depth_ratios = [1, 1]
random.seed(10)

# set compartment heights
heights = [350, 500, 300, 250, 800]

fit_to_size(heights, THICKNESS, HEIGHT)

# example_compartments = [200, 100, 850]
widths_A = [[100, 200, 300, 400], [110, 220, 330, 440], [111, 222, 333, 444], [321, 210, 120]]
# widths_A = [example_compartments] * len(heights)

# print(widths)

all_widths = []

for i in range(len(widths_A)):
	fitted = widths_A[i] + fit_to_size(widths_A[i], THICKNESS, WIDTH)
	all_widths += [fitted]

print("widths = ", all_widths)

compartment_depths = []
extention_intervals = [] # fine a better name.
horizontal_boards = []
vertical_boards = []

# randomly set depth of compartments to DEPTH or DEPTH_EXTRA
for i in range(len(all_widths)):
	line_depths = []
	for j in range(len(all_widths[i])):
		# print("i = {}, j = {}".format(i, j))
		line_depths += random.choices([DEPTH, DEPTH_EXTRA], depth_ratios)
	compartment_depths += [line_depths]


print("compartment depths = ",compartment_depths)


for i in range(len(all_widths)):
	current_intervals = []
	sum_x = THICKNESS
	for j in range(len(all_widths[i])):
		# print("i = {}, j = {}".format(i, j))
		start = sum_x - THICKNESS
		sum_x += all_widths[i][j] + THICKNESS
		if compartment_depths[i][j] == DEPTH_EXTRA:
			end = sum_x
			current_intervals += [[start, end]]
	extention_intervals += [union(current_intervals)]
	# extention_intervals += [current_intervals]

print("extentions intervals", extention_intervals)

print(compartment_depths)
# ypos = 0
# horizontal
# ysum = 