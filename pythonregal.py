#!/usr/bin/env python3

#everything in millimeters

THICKNESS = 20
WIDTH = 2500
HEIGHT = 2500
DEPTH = 400
DEPTH_EXTRA = 500

def board_positions(_list, _th, _maxLength):
	if sum(_list) + (len(_list) + 1) * _th > _maxLength:
		print("the sum of all board sizes plus thickness of boards in between is larger than the allowed size!")
		return 0
	sum_size = 0
	positions = []
	for size in _list:
		sum_size += _th
		start = sum_size
		sum_size += size
		end = sum_size 
		positions += [[start, end]]
	sum_size += _th
	start = sum_size
	end = _maxLength - _th
	positions += [[start, end]]
	return positions

def union(_ranges):
	output = []
	for start, end in sorted(_ranges):
		if output and output[-1][1] >= start - 1:
			output[-1][1] = max(output[-1][1], end)
		else:
			output.append([start, end])
	return output

print(union([[100,300], [200, 400], [500, 600]]))


vertical_compartments = [350, 1000, 150, 250, 300]

vertical_coordinates = board_positions(vertical_compartments, THICKNESS, HEIGHT)

print(vertical_coordinates)

example_compartments = [200, 800, 50]
horizontal_compartments = [[example_compartments] * len(vertical_compartments)]
print(horizontal_compartments)


# n_compartments = len(compartment_heights)

# horizontal_compartments = []

