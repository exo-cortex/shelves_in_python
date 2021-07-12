#!/usr/bin/env python3

import random
import numpy as np
from itertools import accumulate
from shelf_class import Shelf

from shelf_functions import union, fit_to_size

# ++++++++++++++++ setup [millimeters}
# THICKNESS = 20
# WIDTH = 3500
# HEIGHT = 2500
# DEPTH = 400
# DEPTH_EXTRA = 500
# ++++++++++++++++

myshelf = Shelf(thickness=50, fullwidth=2500, fullheight=2500, depth=400, extra_depth=500, random_seed=3)

myshelf.add_level(250, [100, 150, 250, 350, 550, 350])
myshelf.add_level(150, [100, 150, 350, 350, 200, 350])
myshelf.add_level(350, [100, 150, 350, 250, 400, 250])
myshelf.add_level(550, [400, 150, 150, 350,150, 600])
myshelf.add_level(250, [200, 150, 250, 300])
myshelf.add_level(350, [300, 150, 250, 150, 350, 300, 350])
myshelf.fit_to_height([250, 350, 200, 80, 120, 550, 100])
myshelf.fit_to_width()
myshelf.set_depths_randomly(0.25)
# myshelf.shuffle_compartments()
# myshelf.shuffle_levels()

myshelf.accumulate_heights()

# myshelf.set_extra_depth_at([[0,0],[1,1], [2,2], [3,3]])
myshelf.make_boards()
myshelf.calculate_extension_boards()

print(myshelf)

myshelf.write_svg()






