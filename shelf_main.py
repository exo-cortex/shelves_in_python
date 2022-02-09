#!/usr/bin/env python3

import random
import numpy as np
from itertools import accumulate
from shelf_class import Shelf

from shelf_functions import union, fit_to_size

myshelf = Shelf(thickness=18, fullwidth=2500, fullheight=2500, depth=400, extra_depth=550, random_seed=1005, sub_thickness=10)

myshelf.add_level(350, [600, 250, 350, 250, 600])
myshelf.add_level(350, [350, 300, 400, 600])
myshelf.add_level(120, [200, 350, 300, 120, 450, 400])
myshelf.add_level(600, [285, 800, 750, 272])
myshelf.add_level(400, [400, 150, 400, 370, 200, 350])


myshelf.fit_to_height([300, 600, 300, 150, 600])
myshelf.fit_to_width()

# myshelf.shuffle_compartments()
# myshelf.shuffle_levels()
# myshelf.reverse_levels()
# myshelf.set_depths_randomly(0.35)

myshelf.accumulate_heights()
myshelf.accumulate_widths()

myshelf.set_extra_depth_at([ 
	[0,1], [0,5],
	[1,1], [1,4],
	[2,1], [2,3], [2,5],
	[3,0], [3,2], [3,3],
	[4,2], [4,5],
	[5,3], [5, 5],
	])

myshelf.compartment_sub_shelf([
	[3, 3, [600]], [3,0, [150, 150, 150]], 
	[4, 2, [190]]
	])

supportboards = [
	[0,1,0,100], [0,2,0,0], [0,3,100,0], [0,5,0,200], 
	[1,1,50,0], [1,2,100,0], [1,4,0,200],
	[2,1,0,100], [2,2,0,100], [2,4,100,0], [2,6,0,200],
	[3,1,0,100], [3,3,100,0], 
	[4,0,100,0], [4,3,100,0], [ 4, 5, 0, 100],
	[5,0,100,0], [5, 2, 0,150], [5,5,0,200],
	# [6,5,0,200]
]

myshelf.make_boards()
myshelf.calculate_extension_boards()
myshelf.make_support_boards(supportboards)

print(myshelf)

myshelf.material_costs()

myshelf.write_svg()

myshelf.write_cuboids()

myshelf.list_items()

myshelf.print_widths()