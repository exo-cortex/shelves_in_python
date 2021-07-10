
from itertools import accumulate
import random

class Shelf:
	# constants
	DEFAULT_THICKNESS = 20
	DEFAULT_WIDTH = 2500
	DEFAULT_HEIGHT = 2500
	DEFAULT_MIN_HEIGHT = 0
	DEFAULT_DEPTH = 400
	DEFAULT_EXTRA_DEPTH = 500
	DEFAULT_DENSITY = 440.0 # 27.5 kg / (2.5 * 1.25 * 0.02) for Elotis Pine

	def __init__(
		self, 
		thickness=DEFAULT_THICKNESS, 
		fullwidth=DEFAULT_WIDTH,
		fullheight=DEFAULT_HEIGHT,
		min_height=DEFAULT_MIN_HEIGHT,
		depth=DEFAULT_DEPTH,
		extra_depth=DEFAULT_EXTRA_DEPTH
	):
		self.thickness = thickness
		self.fullwidth = fullwidth
		self.fullheight = fullheight
		self.min_height = min_height
		self.depth = depth
		self.extra_depth = extra_depth
		self.levels = 0 # number of vertical compartments
		self.level_heights = [] # heights of each vertical compartment
		self.level_separators = [] # absolute positions
		self.compartments = []
		self.compartment_widths = [] # for each level a list with widths
		self.compartment_separators = [] # list of absolute positions

		# for building
		self.horizontal_boards = []
		self.vertical_boards = []
		self.extension_boards = []

		# for plotting / visualizing
		self.horizaontal_board_coordinates = []
		self.vertical_board_coordinates = []

		# additional operations
		random.seed(1)

	def __str__(self):
		self.account()
		output = ""
		for i in range(self.levels):
			output += "level {}: height = {:4}, {} compartments: widths = {}".format(i, self.level_heights[i], self.compartments[i], self.compartment_widths[i])
			if not i == self.levels - 1:
				output += "\n"
		return output

	def account(self):
		self.levels = len(self.level_heights)
		self.compartments = []
		for i in range(len(self.level_heights)):
			self.compartments += [len(self.compartment_widths[i])]

	def add_level(self, height, widths: list):
		if self.not_too_large(self.level_heights + [height], self.fullheight):
			if self.not_too_large(widths, self.fullwidth):
				self.level_heights += [height]
				self.compartment_widths += [widths]
		self.account()

	def add_compartments_at(self, at_level, widths: list):
		# print(self.compartment_widths[at_level])
		if self.not_too_large(self.compartment_widths[at_level], widths, self.fullwidth):
			self.compartment_widths[at_level] += [1]
			print("lalala", self.compartment_widths[at_level])

	def fit_to_height(self, widths: list=[]):
		if sum(self.level_heights) + (2 + len(self.level_heights)) * self.thickness + self.min_height <= self.fullheight:
			if self.not_too_large(widths, self.fullwidth):
				new_height = self.fullheight - sum(self.level_heights) - (2 + len(self.level_heights)) * self.thickness
				self.level_heights += [new_height]
				extra_width = self.fullwidth - sum(widths) - (2 + len(widths)) * self.thickness
				self.compartment_widths += [widths + [extra_width]]
		self.account()

	def fit_to_width(self, at_level: list=[]):
		if at_level == []:
			for i in range(self.levels):
				new_width = self.fullwidth - sum(self.compartment_widths[i]) - (2 + len(self.compartment_widths[i])) * self.thickness
				self.compartment_widths[i] += [new_width]
		else:
			for i in at_level:
				new_width = self.fullwidth - sum(self.compartment_widths[i]) - (2 + len(self.compartment_widths[i])) * self.thickness
				self.compartment_widths[i] += [new_width]
		self.account()

	def fit(self):
		self.fit_to_height()
		self.fit_to_width()

	def not_too_large(self, sizes: list, total_size):
		return sum(sizes) + (1 + len(sizes)) * self.thickness <= total_size

	def check(self):
		if len(self.level_heights) != len(self.compartment_widths):
			print("ERROR")

	def shuffle_levels(self):
		indices = list(range(len(self.level_heights)))
		random.shuffle(indices)
		self.level_heights = [self.level_heights[i] for i in indices]
		self.compartment_widths = [self.compartment_widths[i] for i in indices]

	def shuffle_compartments(self, at_level: list=[]): # if nothing given shuffle at all levels
		if at_level == []:
			for i in range(len(self.compartment_widths)):
				random.shuffle(self.compartment_widths[i])
		else:
			for i in at_level:
				random.shuffle(self.compartment_widths[i])