import typing
import copy

import constants
import displayer
from game_exceptions import ImpossibleMove
from case import Case


class Board:
    _board = [[]] * 16
    _robot_positions = {}
    _goal_positions = {}

    def __init__(
        self,
        robot_positions: dict,
        goal_positions: dict,
        board: typing.Optional[list] = None,
    ):
        self._robot_positions = robot_positions
        self._goal_positions = goal_positions
        if board:
            self._board = board

    def move_robot(self, robot: constants.Robot, direction: constants.Direction):
        current_i, current_j = self.robot_positions[robot]
        new_i, new_j = current_i, current_j

        while True:
            if not (0 <= new_i < 16 and 0 <= new_j < 16):
                break

            if direction == constants.Direction.DOWN:
                if (constants.Wall.DOWN in self.board[new_i][new_j].walls) or (
                    new_i < 15
                    and (
                        constants.Wall.UP in self.board[new_i + 1][new_j].walls
                        or self.board[new_i + 1][new_j].robot
                    )
                ):
                    break
                new_i += 1
            elif direction == constants.Direction.UP:
                if (constants.Wall.UP in self.board[new_i][new_j].walls) or (
                    new_i > 0
                    and (
                        constants.Wall.DOWN in self.board[new_i - 1][new_j].walls
                        or self.board[new_i - 1][new_j].robot
                    )
                ):
                    break
                new_i -= 1
            elif direction == constants.Direction.RIGHT:
                if (constants.Wall.RIGHT in self.board[new_i][new_j].walls) or (
                    new_j < 15
                    and (
                        constants.Wall.LEFT in self.board[new_i][new_j + 1].walls
                        or self.board[new_i][new_j + 1].robot
                    )
                ):
                    break
                new_j += 1
            elif direction == constants.Direction.LEFT:
                if (constants.Wall.LEFT in self.board[new_i][new_j].walls) or (
                    new_j > 0
                    and (
                        constants.Wall.RIGHT in self.board[new_i][new_j - 1].walls
                        or self.board[new_i][new_j - 1].robot
                    )
                ):
                    break
                new_j -= 1
        if (current_i, current_j) == (new_i, new_j):
            raise ImpossibleMove
        return self.clone_on_move(robot, (new_i, new_j))

    def clone_on_move(self, robot: constants.Robot, robot_position: tuple):
        new_robots_pos = dict(self.robot_positions)
        prev_robot_position = new_robots_pos[robot]
        new_robots_pos[robot] = robot_position

        new_board = Board(new_robots_pos, self.goal_positions, self.board.copy())

        new_board.board[prev_robot_position[0]] = new_board.board[
            prev_robot_position[0]
        ].copy()
        prev_case = new_board.board[prev_robot_position[0]][prev_robot_position[1]]
        new_board.board[prev_robot_position[0]][prev_robot_position[1]] = Case(
            prev_case.i,
            prev_case.j,
            prev_case.goal,
            prev_case.laser,
            prev_case.walls,
            None,
        )

        if robot_position[0] != prev_robot_position[0]:
            new_board.board[robot_position[0]] = new_board.board[
                robot_position[0]
            ].copy()

        new_case = new_board.board[robot_position[0]][robot_position[1]]
        new_board.board[robot_position[0]][robot_position[1]] = Case(
            new_case.i, new_case.j, new_case.goal, new_case.laser, new_case.walls, robot
        )
        return new_board

    def is_goal_reached(self, robot: constants.Robot, goal: constants.Goal):
        return self.robot_positions[robot] == self.goal_positions[goal]

    def display(self, goal: typing.Optional[constants.Goal] = None):
        displayer.Displayer().display(self._board, goal)

    @property
    def board(self):
        return self._board

    @property
    def robot_positions(self):
        return self._robot_positions

    @property
    def goal_positions(self):
        return self._goal_positions
