import typing
import constants
from board import Board
from game_exceptions import ImpossibleMove


class BoardTry:
    leafs = []
    _result_board = None

    def __init__(
        self, root_board: Board, robot: constants.Robot, direction: constants.Direction
    ):
        self.root_board = root_board
        self.robot = robot
        self.direction = direction
        if robot:
            self._result_board = root_board.move_robot(robot, direction)
        else:
            self._result_board = root_board

    def gen_leafs(
        self,
        goal_position: tuple,
        goal: constants.Goal,
        main_robot: constants.Robot,
        other_robots: typing.List[constants.Robot],
        seen_list: set,
    ):
        for direction in constants.Direction:
            try:
                current_try = BoardTry(self.result_board, main_robot, direction)
                if current_try.is_successful(goal_position):
                    return current_try
                if (
                    current_try.result_board.robot_positions[main_robot.value]
                    != self.result_board.robot_positions[main_robot.value]
                ):
                    sorted_positions = tuple(
                        sorted(
                            current_try.result_board.robot_positions,
                            key=lambda k: [k[1], k[0]],
                        )
                    )
                    if sorted_positions not in seen_list:
                        self.leafs.append(current_try)
                        seen_list.add(sorted_positions)
            except ImpossibleMove:
                pass
        for robot in other_robots:
            for direction in constants.Direction:
                try:
                    current_try = BoardTry(self.result_board, robot, direction)
                    if current_try.is_successful(goal_position):
                        return current_try
                    if (
                        current_try.result_board.robot_positions[robot.value]
                        != self.result_board.robot_positions[robot.value]
                    ):
                        sorted_positions = tuple(
                            sorted(
                                current_try.result_board.robot_positions,
                                key=lambda k: [k[1], k[0]],
                            )
                        )
                        if sorted_positions not in seen_list:
                            self.leafs.append(current_try)
                            seen_list.add(sorted_positions)
                except ImpossibleMove:
                    pass
        return None

    def is_successful(self, goal_position: tuple):
        return self.result_board.is_goal_reached(self.robot, goal_position)

    @property
    def result_board(self):
        return self._result_board or self.root_board
