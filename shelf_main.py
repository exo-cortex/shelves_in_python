#!/usr/bin/env python3

import random
import numpy as np
from itertools import accumulate
from shelf_class import Shelf

from shelf_functions import union, fit_to_size

myshelf = Shelf(thickness=20, fullwidth=2500, fullheight=2500, depth=400, extra_depth=550, random_seed=1004, sub_thickness=20)

myshelf.add_level(350, [600, 250, 250, 250, 550, 350])
myshelf.add_level(350, [100, 150, 400, 250, 400, 250])
myshelf.add_level(80, [250, 150, 350, 350, 200, 350])
myshelf.add_level(600, [800, 725, 285, 285])
myshelf.add_level(350, [250, 250, 350, 250, 350, 350])
myshelf.add_level(400, [200, 250, 500, 250, 400])

myshelf.fit_to_height([50, 350, 200, 550, 400])
myshelf.fit_to_width()
# myshelf.shuffle_compartments()
# myshelf.shuffle_levels()

# myshelf.reverse_levels()

myshelf.set_depths_randomly(0.2)
# myshelf.set_extra_depth_at([[3,5]])

myshelf.accumulate_heights()
myshelf.accumulate_widths()

myshelf.compartment_sub_shelf([[4, 2, [190]], [3,4, [200, 150, 150]]])


myshelf.make_boards()
myshelf.calculate_extension_boards()

supportboards = [
    [0,0,50,0], [0, 5, 20, 0], [0, 2, 100, 0], 
    [3,0,0,800-115], [3,0,0,800-115], [3,0,800-115,0], [3,0,800-115,0], [3,1,100,0], 
    [1,1,150,0], [4,3,100,0], [ 4, 5, 0, 250] 
]

myshelf.make_support_boards(supportboards)

print(myshelf)

myshelf.material_costs()

myshelf.write_svg()

myshelf.write_cuboids()