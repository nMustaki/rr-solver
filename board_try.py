import typing
import constants
from board import Board
from game_exceptions import ImpossibleMove


class BoardTry:
    result_board = None

    def __init__(self, root_board: Board, robot: int, direction: int, parent=None):
        self.root_board = root_board
        self.robot = robot
        self.direction = direction
        self.parent = parent
        if robot is not None:
            self.result_board = root_board.move_robot(robot, direction)
        else:
            self.result_board = root_board

    def gen_leaves(
        self,
        goal_position: tuple,
        goal: str,
        robots: typing.List[int],
        seen_positions: set,
        hint_positions: typing.List[tuple],
    ):
        leaves = []
        fast_leaves = []
        for robot in robots:
            main_robot = robots[0] if goal != constants.GOAL_ANY else robot
            for direction in constants.DIRECTIONS:
                try:

                    current_try = BoardTry(self.result_board, robot, direction, self)

                    if robot == main_robot:
                        if current_try.result_board.is_goal_reached(main_robot, goal_position):
                            return current_try, leaves, fast_leaves

                    if tuple(current_try.result_board.robot_positions) not in seen_positions:
                        seen_positions.add(tuple(current_try.result_board.robot_positions))

                        try_robot_pos = current_try.result_board.robot_positions[robot]
                        if (
                            robot == main_robot
                            and (hint_positions[0][0] <= try_robot_pos[0] <= hint_positions[0][1])
                            or (hint_positions[1][0] <= try_robot_pos[1] <= hint_positions[1][1])
                        ):
                            fast_leaves.append(current_try)
                        else:
                            leaves.append(current_try)
                except ImpossibleMove:
                    pass
        return None, leaves, fast_leaves
