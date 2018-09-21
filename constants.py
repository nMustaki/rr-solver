import enum


MAX_TURNS = 10


@enum.unique
class Robot(enum.Enum):
    """Value is also used as index in robot_positions list"""

    GREEN = 0
    BLUE = 1
    YELLOW = 2
    RED = 3


@enum.unique
class Goal(enum.Enum):
    ANY = "any"
    GREEN_PLANET = "Gpl"
    BLUE_PLANET = "Bpl"
    YELLOW_PLANET = "Ypl"
    RED_PLANET = "Rpl"
    GREEN_COGS = "Gco"
    BLUE_COGS = "Bco"
    YELLOW_COGS = "Yco"
    RED_COGS = "Rco"
    GREEN_CIRCLE = "Gci"
    BLUE_CIRCLE = "Bci"
    YELLOW_CIRCLE = "Yci"
    RED_CIRCLE = "Rci"
    GREEN_CROSS = "Gcr"
    BLUE_CROSS = "Bcr"
    YELLOW_CROSS = "Ycr"
    RED_CROSS = "Rcr"


GOAL_PLANET = (Goal.GREEN_PLANET, Goal.BLUE_PLANET, Goal.YELLOW_PLANET, Goal.RED_PLANET)
GOAL_COGS = (Goal.GREEN_COGS, Goal.BLUE_COGS, Goal.YELLOW_COGS, Goal.RED_COGS)
GOAL_CIRCLE = (Goal.GREEN_CIRCLE, Goal.BLUE_CIRCLE, Goal.YELLOW_CIRCLE, Goal.RED_CIRCLE)
GOAL_CROSS = (Goal.GREEN_CROSS, Goal.BLUE_CROSS, Goal.YELLOW_CROSS, Goal.RED_CROSS)


GOAL_TO_ROBOT = {
    Goal.GREEN_PLANET: Robot.GREEN,
    Goal.BLUE_PLANET: Robot.BLUE,
    Goal.YELLOW_PLANET: Robot.YELLOW,
    Goal.RED_PLANET: Robot.RED,
    Goal.GREEN_COGS: Robot.GREEN,
    Goal.BLUE_COGS: Robot.BLUE,
    Goal.YELLOW_COGS: Robot.YELLOW,
    Goal.RED_COGS: Robot.RED,
    Goal.GREEN_CIRCLE: Robot.GREEN,
    Goal.BLUE_CIRCLE: Robot.BLUE,
    Goal.YELLOW_CIRCLE: Robot.YELLOW,
    Goal.RED_CIRCLE: Robot.RED,
    Goal.GREEN_CROSS: Robot.GREEN,
    Goal.BLUE_CROSS: Robot.BLUE,
    Goal.YELLOW_CROSS: Robot.YELLOW,
    Goal.RED_CROSS: Robot.RED,
}


@enum.unique
class Laser(enum.Enum):
    GREEN = 0
    BLUE = 1
    YELLOW = 2
    RED = 3


@enum.unique
class Wall(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


CASE_WALLS = [Wall.RIGHT, Wall.DOWN]


@enum.unique
class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
