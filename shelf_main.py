#!/usr/bin/env python3

import random
import numpy as np
from itertools import accumulate
from shelf_class import Shelf

from shelf_functions import union, fit_to_size

# ++++++++++++++++ setup [millimeters}
THICKNESS = 20
WIDTH = 2500
HEIGHT = 2500
DEPTH = 400
DEPTH_EXTRA = 500
# ++++++++++++++++

myshelf = Shelf(thickness=20, fullwidth=2500, fullheight=2500, depth=400, extra_depth=500)

myshelf.add_level(150, [100, 350, 750, 400])
myshelf.add_level(250, [200, 250, 750, 300])
myshelf.add_level(350, [300, 150, 250, 350, 300, 350])
myshelf.add_level(450, [400, 150, 150, 350, 500])
myshelf.fit_to_height([250, 350, 200, 80, 120, 500])

myshelf.shuffle_levels()
myshelf.shuffle_compartments()
print(myshelf)


# lists:
# heights
# widths
# horizontal boards
# vertical boards

# depth_ratios = [1, 1]
# random.seed(10)

# # set compartment heights
# set_heights = [350, 500, 300, 250, 800]

# heights = fit_to_size(set_heights, THICKNESS, HEIGHT)
# print("{} levels: {}".format(len(heights), heights))


# print("++++++++++++++++")
# # example_compartments = [200, 100, 850]
# widths_A = [[100, 200, 300, 400], [750, 250, 330, 150], [350, 200, 300, 400], [250, 300, 100, 100, 100], [500, 200, 750], [500, 200, 750, 250]]
# # widths_A = [example_compartments] * len(heights)

# # print(widths)

# all_widths = []

# for i in range(len(widths_A)):
# 	fitted = widths_A[i] + fit_to_size(widths_A[i], THICKNESS, WIDTH)
# 	all_widths += [fitted]

# # print("widths = ", all_widths)

# compartment_depths = []
# extension_intervals = [] # fine a better name.
# horizontal_cuboids = []
# extra_boards = []
# vertical_cuboids = []

# # randomly set depth of compartments to DEPTH or DEPTH_EXTRA
# for i in range(len(all_widths)):
# 	line_depths = []
# 	for j in range(len(all_widths[i])):
# 		# print("i = {}, j = {}".format(i, j))
# 		line_depths += random.choices([DEPTH, DEPTH_EXTRA], depth_ratios)
# 	compartment_depths += [line_depths]

# # print("compartment depths = ",compartment_depths)

# # for compartments with DEPTH_EXTRA calculate [left-thickness, right+thickness]
# for i in range(len(all_widths)):
# 	current_intervals = []
# 	sum_x = THICKNESS
# 	for j in range(len(all_widths[i])):
# 		# print("i = {}, j = {}".format(i, j))
# 		start = sum_x - THICKNESS
# 		sum_x += all_widths[i][j] + THICKNESS
# 		if compartment_depths[i][j] == DEPTH_EXTRA:
# 			end = sum_x
# 			current_intervals += [[start, end]]
# 	extension_intervals += [union(current_intervals)]
# 	# extension_intervals += [current_intervals]

# # print("extensions intervals", extension_intervals)

# # combine intervals of adjacent levels
# combined_extensions_intervals = [extension_intervals[0]]
# for i in range(len(extension_intervals) - 1):
# 	# print("{}".format(i))
# 	# print(extension_intervals[i])
# 	# print(extension_intervals[i] + extension_intervals[i + 1])
# 	# print(union(extension_intervals[i] + extension_intervals[i + 1]))
# 	combined_extensions_intervals += [union(extension_intervals[i] + extension_intervals[i + 1])]

# combined_extensions_intervals += [extension_intervals[-1]]
# # print(combined_extensions_intervals)

# sum_y = 0
# yi = 0
# horizontal_area = 0
# vertical_area = 0
# volume = 0
# for i in range(len(heights)):
# 	LLB = [0, sum_y, 0] # lower left back
# 	sum_y += THICKNESS
# 	URF = [WIDTH, sum_y, DEPTH] # upper right front
# 	horizontal_cuboids += [[LLB, URF]]
# 	horizontal_area += (URF[0] - LLB[0]) * (URF[2] - LLB[2]) / 1000000.0
# 	volume += (URF[0] - LLB[0]) * (URF[1] - LLB[1]) * (URF[2] - LLB[2]) / 1000000000.0
# 	print("extensions ", combined_extensions_intervals[i])

# 	sum_x = 0
# 	print(i)
# 	for width in all_widths[i]:
# 		LLB = [sum_x, sum_y, 0]
# 		sum_x += THICKNESS
# 		URF = [sum_x, sum_y + heights[i], DEPTH] 
# 		vertical_cuboids += [[LLB, URF]]
# 		vertical_area += (URF[1] - LLB[1]) * (URF[2] - LLB[2]) / 1000000.0
# 		volume += (URF[0] - LLB[0]) * (URF[1] - LLB[1]) * (URF[2] - LLB[2]) / 1000000000.0
# 		sum_x += width
		
# 	LLB = [sum_x, sum_y, 0] 
# 	sum_y += heights[i]
# 	URF = [sum_x + THICKNESS, sum_y, DEPTH]
# 	vertical_cuboids += [[LLB, URF]]
# 	vertical_area += (URF[1] - LLB[1]) * (URF[2] - LLB[2]) / 1000000.0
# 	volume += (URF[0] - LLB[0]) * (URF[1] - LLB[1]) * (URF[2] - LLB[2]) / 1000000000.0
# 	yi += 1

# LLB = [0, sum_y, 0]
# URF = [WIDTH, sum_y + THICKNESS, DEPTH]
# horizontal_cuboids += [[LLB, URF]]
# horizontal_area += (URF[0] - LLB[0]) * (URF[1] - LLB[1]) / 1000000.0
# volume += (URF[0] - LLB[0]) * (URF[1] - LLB[1]) * (URF[2] - LLB[2]) / 1000000000.0

# print("\nhorizontal boards ", horizontal_cuboids, "\nnumber: ", len(horizontal_cuboids), " area = ", horizontal_area)
# print("\nvertical boards ", vertical_cuboids, "\nnumber: ", len(vertical_cuboids), "area = ", vertical_area)
# print("\nvolume = ", volume, " weight = ", volume * 440.0)

