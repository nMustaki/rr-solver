import typing

import constants
import displayer
from game_exceptions import ImpossibleMove
from case import Case


class Board:
    board = [[]] * 16
    robot_positions = None

    def __init__(
        self,
        robot_positions: typing.List[constants.Robot],
        board: typing.Optional[list] = None,
    ):
        self.robot_positions = robot_positions
        if board:
            self.board = board

    def move_robot(self, robot: constants.Robot, direction: constants.Direction):
        current_i, current_j = self.robot_positions[robot.value]
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
        new_robots_pos = self.robot_positions.copy()
        prev_robot_position = new_robots_pos[robot.value]
        new_robots_pos[robot.value] = robot_position

        new_board = Board(new_robots_pos, self.board.copy())

        new_board.board[prev_robot_position[0]] = new_board.board[
            prev_robot_position[0]
        ].copy()
        prev_case = new_board.board[prev_robot_position[0]][prev_robot_position[1]]
        new_board.board[prev_robot_position[0]][prev_robot_position[1]] = Case(
            prev_case.i, prev_case.j, prev_case.walls, None
        )

        if robot_position[0] != prev_robot_position[0]:
            new_board.board[robot_position[0]] = new_board.board[
                robot_position[0]
            ].copy()

        new_case = new_board.board[robot_position[0]][robot_position[1]]
        new_board.board[robot_position[0]][robot_position[1]] = Case(
            new_case.i, new_case.j, new_case.walls, robot
        )
        return new_board

    def is_goal_reached(self, robot: constants.Robot, goal_position: tuple):
        return self.robot_positions[robot.value] == goal_position

    def display(self, goal_positions, goal: typing.Optional[constants.Goal] = None):
        displayer.Displayer().display(self.board, goal_positions, goal)
