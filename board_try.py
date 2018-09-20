import typing
import constants
from board import Board
from game_exceptions import ImpossibleMove


class BoardTry:
    _leafs = []
    _result_board = None

    def __init__(
        self, root_board: Board, robot: constants.Robot, direction: constants.Direction
    ):
        self._root_board = root_board
        self._robot = robot
        self._direction = direction
        if robot:
            self._result_board = root_board.move_robot(robot, direction)
        else:
            self._result_board = root_board

    def gen_leafs(
        self,
        goal: constants.Goal,
        main_robot: constants.Robot,
        other_robots: typing.List[constants.Robot],
    ):
        for direction in constants.Direction:
            try:
                current_try = BoardTry(self.result_board, main_robot, direction)
                if current_try.is_successful(goal):
                    return current_try
                self._leafs.append(current_try)
            except ImpossibleMove:
                pass
        for robot in other_robots:
            for direction in constants.Direction:
                try:
                    current_try = BoardTry(self.result_board, robot, direction)
                    if current_try.is_successful(goal):
                        return current_try
                    self._leafs.append(current_try)
                except ImpossibleMove:
                    pass
        return None

    def is_successful(self, goal: constants.Goal):
        return self.result_board.is_goal_reached(self._robot, goal)

    @property
    def root_board(self):
        return self._root_board

    @property
    def result_board(self):
        return self._result_board or self.root_board

    @property
    def leafs(self):
        return self._leafs
