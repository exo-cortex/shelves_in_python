
from itertools import accumulate
import random
from shelf_functions import union

class Shelf:
	# constants
	DEFAULT_THICKNESS = 20
	DEFAULT_SUB_THICKNESS = 10
	DEFAULT_WIDTH = 2500
	DEFAULT_HEIGHT = 2500
	DEFAULT_MIN_HEIGHT = 100
	DEFAULT_DEPTH = 400
	DEFAULT_EXTRA_DEPTH = 500
	DEFAULT_DENSITY = 600.0 # 27.5 kg / (2.5 * 1.25 * 0.02) for Elotis Pine
	DEFAULT_RANDOM_SEED = 0

	def __init__(
		self, 
		thickness=DEFAULT_THICKNESS,
		sub_thickness=DEFAULT_SUB_THICKNESS,
		fullwidth=DEFAULT_WIDTH,
		fullheight=DEFAULT_HEIGHT,
		min_height=DEFAULT_MIN_HEIGHT,
		depth=DEFAULT_DEPTH,
		extra_depth=DEFAULT_EXTRA_DEPTH,
		random_seed=DEFAULT_RANDOM_SEED
	):
		self.thickness = thickness
		self.sub_thickness = sub_thickness
		self.fullwidth = fullwidth
		self.fullheight = fullheight
		self.min_height = min_height
		self.depth = depth
		self.extra_depth = extra_depth
		self.levels = 0 # number of vertical compartments
		self.level_heights = [] # heights of each vertical compartment
		self.accumulated_heights = []
		self.accumulated_widths = []
		self.level_separators = [] # absolute positions
		self.compartments = []
		self.compartment_widths = [] # for each level a list with widths
		self.compartment_separators = [] # list of absolute positions
		self.compartment_depths = []
		self.combined_level_intervals = []

		# for building
		self.horizontal_boards = []
		self.vertical_boards = []
		self.extension_boards = []
		self.support_boards = []

		# for plotting / visualizing
		self.horizontal_board_coordinates = []
		self.horizontal_extra_board_coordinates = []
		self.vertical_board_coordinates = []
		self.vertical_extra_board_coordinates = []
		self.per_compartment_horizontal_boards = []
		self.support_board_coordinates = []
		self.vertical_boards_sorted = []
		self.support_board_coordinates_sorted = []
		self.horizontal_extra_board_coordinates_sorted = []

		self.random_seed = random_seed
		# additional operations
		random.seed(random_seed)

	def __str__(self):
		self.account()
		output = ""
		for l in range(self.levels):
			output += "level {}: levelheight = {:4}, height = {:4}, width = {:4}, {} compartments: [".format(l, self.level_heights[l], self.accumulated_heights[l] , self.accumulated_widths[l][-1], self.compartments[l]) 
			for c in range(self.compartments[l]):
				marker = " "
				if self.compartment_depths[l][c] == self.extra_depth:
					marker = "x"
				output += " {}{}".format(self.compartment_widths[l][c], marker)
			output += "]"
			if not l == self.levels - 1:
				output += "\n"
		return output

	def account(self):
		self.levels = len(self.level_heights)
		self.compartments = []
		for i in range(len(self.level_heights)):
			self.compartments += [len(self.compartment_widths[i])]

	def accumulate_heights(self):
		self.accumulated_heights = []
		y = 0
		self.accumulated_heights += [y]
		for height in self.level_heights:
			y += self.thickness + height
			self.accumulated_heights += [y]

	def accumulate_widths(self):
		self.accumulated_widths = []
		for l in range(self.levels):
			x = 0
			accumulated_widths = [x]
			for width in self.compartment_widths[l]:
				x += width + self.thickness
				accumulated_widths += [x]
			self.accumulated_widths += [accumulated_widths]			

	def add_level(self, height, widths: list):
		if self.not_too_large(self.level_heights + [height], self.fullheight):
			if self.not_too_large(widths, self.fullwidth):
				self.level_heights += [height]
				self.compartment_widths += [widths]
				self.compartment_depths += [[self.depth] * len(widths)]
		self.account()

	def fit_to_height(self, widths: list=[]):
		if sum(self.level_heights) + (2 + len(self.level_heights)) * self.thickness + self.min_height <= self.fullheight:
			if self.not_too_large(widths, self.fullwidth):
				new_height = self.fullheight - sum(self.level_heights) - (2 + len(self.level_heights)) * self.thickness
				self.level_heights += [new_height]
				rest_width = self.fullwidth - sum(widths) - (2 + len(widths)) * self.thickness
				# print("rest width ", rest_width)
				# print([widths + [rest_width]])
				self.compartment_widths += [widths + [rest_width]]
				self.compartment_depths += [[self.depth] * (1 + len(widths))]
		self.account()

	def fit_to_width(self, at_level: list=[]):			
		if at_level == []:
			at_level = [i for i in range(self.levels)]
			for i in at_level:
				current_width = sum(self.compartment_widths[i]) + (2 + len(self.compartment_widths[i])) * self.thickness
				if current_width < self.fullwidth:
					new_width = self.fullwidth - current_width
					self.compartment_widths[i] += [new_width]
					self.compartment_depths[i] += [self.depth]
		self.account()
		for i in range(self.levels):
			sum_widths = sum(self.compartment_widths[i])
			n_boards = 1+len(self.compartment_widths[i])
			# print("level {}, sum(widths)={} ({}), num of boards={}".format(i, sum_widths, sum_widths + n_boards * self.thickness, n_boards))

	def set_depths_randomly(self, p):
		for l in range(self.levels):
			for c in range(self.compartments[l]):
				depth = random.choices([self.depth, self.extra_depth], [1 - p, p])
				self.compartment_depths[l][c] = depth[0]


	def set_extra_depth_at(self, at_index: list=[]):
		for l, c in at_index:
			self.compartment_depths[l][c] = self.extra_depth

	def compartment_sub_shelf(self, at_what: list=[]):
		self.per_compartment_horizontal_boards = []
		for yi, xi, hs in at_what:
			ysub = 0
			for h in hs:
				ysub += h
				sub_LBB = [self.accumulated_widths[yi][xi] + self.thickness, self.accumulated_heights[yi] + ysub, self.thickness]
				ysub += self.sub_thickness
				sub_RTF = [self.accumulated_widths[yi][xi + 1], self.accumulated_heights[yi] + ysub, self.compartment_depths[yi][xi]]
				self.per_compartment_horizontal_boards += [[sub_LBB, sub_RTF]]

	def fit(self):
		self.fit_to_height()
		self.fit_to_width()

	def not_too_large(self, sizes: list, total_size):
		return sum(sizes) + (1 + len(sizes)) * self.thickness <= total_size

	def reverse_levels(self):
		self.level_heights = [h for h in reversed(self.level_heights)]
		self.compartment_widths = [cw for cw in reversed(self.compartment_widths)]
		self.compartment_depths = [cd for cd in reversed(self.compartment_depths)]
		self.compartments = [c for c in reversed(self.compartments)]

	def shuffle_levels(self):
		indices = list(range(len(self.level_heights)))
		random.shuffle(indices)
		self.level_heights = [self.level_heights[i] for i in indices]
		self.compartment_widths = [self.compartment_widths[i] for i in indices]
		self.compartment_depths = [self.compartment_depths[i] for i in indices]
		self.compartments = [self.compartments[i] for i in indices]
		self.account()

	def shuffle_compartments(self, at_level: list=[]):
		if at_level == []:
			at_level = range(self.levels)
		for i in at_level:
			indices = list(range(len(self.compartment_widths[i])))
			random.shuffle(indices)
			self.compartment_widths[i] = [self.compartment_widths[i][j] for j in indices]
			self.compartment_depths[i] = [self.compartment_depths[i][j] for j in indices]
		self.account()

	def make_boards(self):
		y = 0
		for yi in range(self.levels):
			temp_vertical_boards = []
			h_LBB = [0, y, 0]
			h_RTF = [self.fullwidth, y + self.thickness, self.depth]
			x = 0
			height = self.level_heights[yi]
			last_depth = self.compartment_depths[yi][0]
			for xi in range(self.compartments[yi]):
				v_LBB = [x, y + self.thickness, 0]
				# v_RTF = [x + self.thickness, y + self.thickness + height, self.compartment_depths[yi][xi]]
				depth = max(last_depth, self.compartment_depths[yi][xi])
				v_RTF = [x + self.thickness, y + self.thickness + height, depth]
				if self.compartment_depths[yi][xi] == self.extra_depth or last_depth == self.extra_depth:
					self.vertical_extra_board_coordinates += [[v_LBB, v_RTF]] 
				else:
					self.vertical_board_coordinates += [[v_LBB, v_RTF]]
				temp_vertical_boards += [[v_LBB, v_RTF]]
				last_depth = self.compartment_depths[yi][xi]
				x += self.compartment_widths[yi][xi] + self.thickness
			v_LBB = [x, y + self.thickness, 0]
			v_RTF = [x + self.thickness, y + self.thickness + height, last_depth]
			if last_depth == self.extra_depth:
				self.vertical_extra_board_coordinates += [[v_LBB, v_RTF]] 
			else:
				self.vertical_board_coordinates += [[v_LBB, v_RTF]]
			temp_vertical_boards += [[v_LBB, v_RTF]]
			self.vertical_boards_sorted += [[yi, temp_vertical_boards]]
			self.vertical_board_coordinates += [[v_LBB, v_RTF]]
			self.horizontal_board_coordinates += [[h_LBB, h_RTF]]
			y += height + self.thickness
		h_LBB = [0, y, 0]
		h_RTF = [self.fullwidth, y + self.thickness, self.depth]
		self.horizontal_board_coordinates += [[h_LBB, h_RTF]]

	def make_support_boards(self, at: list=[]):
		self.accumulate_widths()
		self.support_board_coordinates = []
		for yi, xi, dstart, dend in at:
			s_LBB = [self.accumulated_widths[yi][xi] + self.thickness + dstart, self.accumulated_heights[yi] + self.thickness, 0]
			s_RTF = [self.accumulated_widths[yi][xi + 1] - dend, self.accumulated_heights[yi + 1], self.thickness]
			# print([[s_LBB, s_RTF]])
			self.support_board_coordinates += [[s_LBB, s_RTF]]
			self.support_board_coordinates_sorted += [[yi, [[s_LBB, s_RTF]]]]
		# print(self.support_board_coordinates)

	def find_combined_extension_intervals(self):
		level_intervals = []
		for yi in range(self.levels):
			intervals = []
			start = 0
			end = 0
			for xi, width in enumerate(self.compartment_widths[yi]):
				end += self.thickness + width
				if self.compartment_depths[yi][xi] == self.extra_depth:
					intervals += [[start, end + self.thickness]]
				start = end
			level_intervals += [[yi, union(intervals)]]
		# print(level_intervals)
		self.combined_level_intervals += [level_intervals[0]]
		for yi in range(self.levels - 1):
			# print("_level ", yi, level_intervals[yi])
			# print("level ", yi, union(level_intervals[yi][1] + level_intervals[yi + 1][1]))
			self.combined_level_intervals += [[yi + 1, union(level_intervals[yi][1] + level_intervals[yi + 1][1])]]
		self.combined_level_intervals += [[self.levels, level_intervals[self.levels - 1][1]]]

	def calculate_extension_boards(self):
		self.accumulate_heights()
		self.find_combined_extension_intervals()
		self.make_horizontal_extension_boards()

	def make_horizontal_extension_boards(self):
		for yi, intervals in self.combined_level_intervals:
			for interval in intervals:
				e_LBB = [interval[0], self.accumulated_heights[yi], self.depth]
				e_RTF = [interval[1], self.accumulated_heights[yi] + self.thickness, self.extra_depth]
				self.horizontal_extra_board_coordinates += [[e_LBB, e_RTF]]
				self.horizontal_extra_board_coordinates_sorted += [[yi, [[e_LBB, e_RTF]]]]

	def material_costs(self):
		print("extenter schrauben: ", 4 * sum([compartments + 1 for compartments in self.compartments]))
		# print(self.levels + 1," horizontal boards", (self.leves + 1) * 2.5 * 1.25 * 0.02 )
		density = 600
		# print(density)
		volume = 0
		weight = 0
		combined_list = self.horizontal_board_coordinates + self.horizontal_extra_board_coordinates + self.vertical_board_coordinates + self.vertical_extra_board_coordinates + self.support_board_coordinates + self.per_compartment_horizontal_boards
		for [[xmin, ymin, zmin], [xmax, ymax, zmax]] in combined_list:
			vol = (xmax - xmin) * (ymax - ymin) * (zmax - zmin)
			# print("horizontal boards", [[xmin, ymin, zmin], [xmax, ymax, zmax]], vol, vol*density)
			volume += vol
			weight += vol * density / 1000000000.0
		print("volume = ", volume / 1e9, "m^3, weight = ", weight)
		print("platten [2500x1250x20] ", volume/(2500 * 1250 * 20), "price = ", volume/(2500 * 1250 * 20) * 60)
		# print(density)

	def write_svg(self, filename: str="shelf.svg"):
		file = open(filename, "w")
		svg_header = '<?xml version="1.0" encoding="utf-8" ?>'
		svg_header += '<svg xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink" '
		padding = 50
		svg_header += 'baseProfile="tiny" version="1.2" '
		svg_header += 'width="100%" height="100%" viewBox="{},{},{},{}">'.format(0 - padding/2, 0 - padding/2, self.fullwidth + padding, self.fullheight + padding)
		svg_defs = '<defs />'
		file.write(svg_header)
		file.write(svg_defs)

		def write_grid(col, sw):
			meter = 1000
			sub = 100
			th = sw
			for i in range(0, self.fullwidth, meter): 
				th = sw
				for j in range(0, meter, sub):
					if j > 0: 
						th = sw * 0.25
					file.write('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="{}" />'.format(i + j, 0, i + j, self.fullheight, col, th))
			for i in range(0, self.fullheight, meter):
				th = sw
				for j in range(0, meter, sub):
					if j > 0: 
						th = sw * 0.25
					file.write('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="{}" />'.format(0, self.fullheight - i - j, self.fullwidth, self.fullheight - i - j, col, th))

		def write_rec(col, xmin, ymin, xmax, ymax):
			xleft, xright = xmin, xmax - xmin
			ylow, ytop = self.fullheight - ymin, self.fullheight - ymax 
			file.write('<rect fill="{}" x="{}" y="{}" width="{}" height="{}"/>'.format(col, xleft, ytop, xright, ylow - ytop))

		background_color = "#FFFFFF"
		write_rec(background_color, 0 - padding/2, 0 - padding/2, self.fullwidth + padding, self.fullheight + padding)

		h_color = "#000000"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.horizontal_board_coordinates:
			write_rec(h_color, xmin, ymin, xmax, ymax)

		e_color = "#0000ff"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.horizontal_extra_board_coordinates:
			write_rec(e_color, xmin, ymin, xmax, ymax)

		v_color = "#000000"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.vertical_board_coordinates:
			write_rec(v_color, xmin, ymin, xmax, ymax)

		ve_color = "#0000ff"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.vertical_extra_board_coordinates:
			write_rec(ve_color, xmin, ymin, xmax, ymax)

		s_color = "#FF0000AA"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.support_board_coordinates:
			write_rec(s_color, xmin, ymin, xmax, ymax)

		sub_color = "#00FF00"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.per_compartment_horizontal_boards:
			write_rec(sub_color, xmin, ymin, xmax, ymax)

		write_grid("#000000", 4)

		file.write('</svg>')
		file.close()

	def write_cuboids(self):
		combined_list = self.horizontal_board_coordinates + self.horizontal_extra_board_coordinates + self.vertical_board_coordinates + self.vertical_extra_board_coordinates + self.support_board_coordinates + self.per_compartment_horizontal_boards
		file = open("cuboids.txt", "w")
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in combined_list:
			file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(xmin,ymin,zmin,xmax,ymax,zmax))

	def list_items(self):
		count_boards = 0
		area = 0

		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.horizontal_board_coordinates:
			print("horizontal board: ", xmax-xmin, "mm x ", zmax-zmin, "mm")
			count_boards += 1
			# area += xmax-xmin * zmax-zmin * (1/1000000)

		upto = 3
		for level, boards in self.horizontal_extra_board_coordinates_sorted:
			if level < upto:
				for [xmin, ymin, zmin],[xmax, ymax, zmax] in boards:
					print("level: ", level, " horizontal extension: ", xmax-xmin, "mm x ", zmax-zmin, "mm")
					count_boards += 1
					area += (xmax-xmin) * (zmax-zmin) * (1/1000000)

		# print(self.vertical_boards_sorted)
		for level, boards in self.vertical_boards_sorted:
			if level < upto:
				for [xmin, ymin, zmin],[xmax, ymax, zmax] in boards:
					print("level: ", level, " board: ", zmax-zmin, "mm x ", ymax-ymin, "mm")
					count_boards += 1
					area += (zmax-zmin) * (ymax-ymin) * (1/1000000)

		for level, boards in self.support_board_coordinates_sorted:
			if level < upto:
				for [xmin, ymin, zmin],[xmax, ymax, zmax] in boards:
					print("level: ", level, " supportboard: ", xmax-xmin, "mm x ", ymax-ymin, "mm")
					count_boards += 1
					area += (xmax-xmin) * (ymax-ymin) * (1/1000000)

		print("number of boards = ", count_boards, ", costs = ", 0.5 * count_boards)
		print("area = ", area, ", cost = ", area*33.9)
