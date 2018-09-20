import typing

import constants

I_IDX = 0
J_IDX = 1
GOAL_IDX = 2
LASER_IDX = 3
WALLS_IDX = 4
ROBOT_IDX = 5

from collections import namedtuple

Case = namedtuple("case2", ["i", "j", "goal", "laser", "walls", "robot"])
