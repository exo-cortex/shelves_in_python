
from itertools import accumulate
import random
from shelf_functions import union

class Shelf:
	# constants
	DEFAULT_THICKNESS = 20
	DEFAULT_WIDTH = 2500
	DEFAULT_HEIGHT = 2500
	DEFAULT_MIN_HEIGHT = 100
	DEFAULT_DEPTH = 400
	DEFAULT_EXTRA_DEPTH = 500
	DEFAULT_DENSITY = 440.0 # 27.5 kg / (2.5 * 1.25 * 0.02) for Elotis Pine
	DEFAULT_RANDOM_SEED = 0

	def __init__(
		self, 
		thickness=DEFAULT_THICKNESS, 
		fullwidth=DEFAULT_WIDTH,
		fullheight=DEFAULT_HEIGHT,
		min_height=DEFAULT_MIN_HEIGHT,
		depth=DEFAULT_DEPTH,
		extra_depth=DEFAULT_EXTRA_DEPTH,
		random_seed=DEFAULT_RANDOM_SEED
	):
		self.thickness = thickness
		self.fullwidth = fullwidth
		self.fullheight = fullheight
		self.min_height = min_height
		self.depth = depth
		self.extra_depth = extra_depth
		self.levels = 0 # number of vertical compartments
		self.level_heights = [] # heights of each vertical compartment
		self.accumulated_heights = []
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

		self.random_seed = random_seed
		# additional operations
		random.seed(random_seed)

	def __str__(self):
		self.account()
		output = ""
		for l in range(self.levels):
			output += "level {}: height = {:4}, {} compartments: [".format(l, self.level_heights[l], self.compartments[l]) 
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
		# print(self.level_heights)
		for height in self.level_heights:
			y += self.thickness + height
			self.accumulated_heights += [y]

	def add_level(self, height, widths: list):
		if self.not_too_large(self.level_heights + [height], self.fullheight):
			if self.not_too_large(widths, self.fullwidth):
				self.level_heights += [height]
				self.compartment_widths += [widths]
				self.compartment_depths += [[self.depth] * len(widths)]
		self.account()

	# def add_compartments_at(self, at_level, widths: list):
	# 	# print(self.compartment_widths[at_level])
	# 	if self.not_too_large(self.compartment_widths[at_level], widths, self.fullwidth):
	# 		self.compartment_widths[at_level] += [1]
	# 		print("lalala", self.compartment_widths[at_level])
	# 	self.account()

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
		# print(self.compartment_depths)

	def set_extra_depth_at(self, at_index: list=[]):
		# print(self.compartment_depths)
		for l, c in at_index:
			self.compartment_depths[l][c] = self.extra_depth
			# print("[{}, {}]".format(l, c))

	def fit(self):
		self.fit_to_height()
		self.fit_to_width()

	def not_too_large(self, sizes: list, total_size):
		return sum(sizes) + (1 + len(sizes)) * self.thickness <= total_size

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
			h_LBB = [0, y, 0]
			h_RTF = [self.fullwidth, y + self.thickness, self.depth]
			x = 0
			height = self.level_heights[yi]
			last_depth = self.compartment_depths[yi][0]
			for xi in range(self.compartments[yi]):
				v_LBB = [x, y + self.thickness, self.compartment_depths[yi][xi]]
				v_RTF = [x + self.thickness, y + self.thickness + height, self.compartment_depths[yi][xi]]
				# print("next board: ", [[v_LBB, v_RTF]])
				if self.compartment_depths[yi][xi] == self.extra_depth or last_depth == self.extra_depth:
					self.vertical_extra_board_coordinates += [[v_LBB, v_RTF]] 
				else:
					self.vertical_board_coordinates += [[v_LBB, v_RTF]]
				last_depth = self.compartment_depths[yi][xi]
				x += self.compartment_widths[yi][xi] + self.thickness
			v_LBB = [x, y + self.thickness, last_depth]
			v_RTF = [x + self.thickness, y + self.thickness + height, last_depth]
			if last_depth == self.extra_depth:
				self.vertical_extra_board_coordinates += [[v_LBB, v_RTF]] 
			else:
				self.vertical_board_coordinates += [[v_LBB, v_RTF]]
			self.vertical_board_coordinates += [[v_LBB, v_RTF]]
			self.horizontal_board_coordinates += [[h_LBB, h_RTF]]
			y += height + self.thickness
		h_LBB = [0, y, 0]
		h_RTF = [self.fullwidth, y + self.thickness, self.depth]
		self.horizontal_board_coordinates += [[h_LBB, h_RTF]]

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
			# print(self.accumulated_heights[yi], " - ", intervals)
			for interval in intervals:
				# print(i, " interval", interval)
				# print("first entry: ", interval[0])
				# if len(interval) > 0:
				e_LBB = [interval[0], self.accumulated_heights[yi], self.depth]
				e_RTF = [interval[1], self.accumulated_heights[yi] + self.thickness, self.extra_depth]
				# print("next board: ", e_LBB, e_RTF)
				self.horizontal_extra_board_coordinates += [[e_LBB, e_RTF]]
				# print(self.accumulated_heights[yi], interval)
		# # print("interval ", intervals)
		print("extension boards : ", self.horizontal_extra_board_coordinates)

	def write_svg(self, filename: str="shelf.svg"):
		file = open(filename, "w")
		svg_header = '<?xml version="1.0" encoding="utf-8" ?>'
		svg_header += '<svg xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink" '
		svg_header += 'baseProfile="tiny" version="1.2" '
		svg_header += 'width="100%" height="100%" viewBox="{},{},{},{}">'.format(0, 0, self.fullwidth, self.fullheight)
		svg_defs = '<defs />'

		file.write(svg_header)
		file.write(svg_defs)

		h_color = "#000000"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.horizontal_board_coordinates:
			file.write('<rect fill="{}" x="{}" y="{}" width="{}" height="{}"/>'.format(h_color, xmin, ymin, xmax - xmin, ymax - ymin))

		e_color = "#0000ff"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.horizontal_extra_board_coordinates:
			file.write('<rect fill="{}" x="{}" y="{}" width="{}" height="{}"/>'.format(e_color, xmin, ymin, xmax - xmin, ymax - ymin))

		v_color = "#000000"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.vertical_board_coordinates:
			file.write('<rect fill="{}" x="{}" y="{}" width="{}" height="{}"/>'.format(v_color, xmin, ymin, xmax - xmin, ymax - ymin))

		ve_color = "#0000ff"
		for [[xmin, ymin, zmin],[xmax, ymax, zmax]] in self.vertical_extra_board_coordinates:
			file.write('<rect fill="{}" x="{}" y="{}" width="{}" height="{}"/>'.format(ve_color, xmin, ymin, xmax - xmin, ymax - ymin))

		file.write('</svg>')

		file.close()
