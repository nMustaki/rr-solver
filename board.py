import typing

import constants
import displayer
from game_exceptions import ImpossibleMove
from case import Case


class Board:
    board = None  # [[]] * 16
    robot_positions = None

    def __init__(self, robot_positions: typing.List[int], board: typing.Optional[list] = None):
        self.robot_positions = robot_positions
        if board:
            self.board = board

    def move_robot(self, robot: int, direction: int):
        current_i, current_j = self.robot_positions[robot]
        new_i, new_j = current_i, current_j
        # if (current_i, current_j) == (6, 0) and robot == constants.ROBOT_RED and direction == constants.DIRECTION_UP:
        #     if self.robot_positions[constants.ROBOT_YELLOW] == (2, 0) and self.robot_positions[
        #         constants.ROBOT_GREEN
        #     ] == (3, 3):
        #         import ipdb

        #         ipdb.set_trace()
        while True:
            if not (0 <= new_i < 16 and 0 <= new_j < 16):
                break

            current_walls = self.board[new_i][new_j].walls

            if direction == constants.DIRECTION_DOWN:
                if (constants.WALL_DOWN in current_walls) or (
                    new_i < 15 and (self.board[new_i + 1][new_j].robot is not None)
                ):
                    break
                new_i += 1
            elif direction == constants.DIRECTION_UP:
                if (constants.WALL_UP in current_walls) or (
                    new_i > 0 and (self.board[new_i - 1][new_j].robot is not None)
                ):
                    break
                new_i -= 1
            elif direction == constants.DIRECTION_RIGHT:
                if (constants.WALL_RIGHT in current_walls) or (
                    new_j < 15 and (self.board[new_i][new_j + 1].robot is not None)
                ):
                    break
                new_j += 1
            elif direction == constants.DIRECTION_LEFT:
                if (constants.WALL_LEFT in current_walls) or (
                    new_j > 0 and (self.board[new_i][new_j - 1].robot is not None)
                ):
                    break
                new_j -= 1

        if (current_i, current_j) == (new_i, new_j):
            raise ImpossibleMove
        # print("...", robot, direction, (current_i, current_j), (new_i, new_j))
        return self.clone_on_move(robot, (new_i, new_j))

    def clone_on_move(self, robot: int, robot_position: tuple):
        new_robots_pos = self.robot_positions.copy()
        prev_robot_position = self.robot_positions[robot]
        new_robots_pos[robot] = robot_position

        prev_i, prev_j = prev_robot_position[0], prev_robot_position[1]

        new_board = Board(new_robots_pos, self.board.copy())

        new_board.board[prev_i] = new_board.board[prev_i].copy()
        prev_case = new_board.board[prev_i][prev_j]
        new_board.board[prev_i][prev_j] = Case(prev_case.i, prev_case.j, prev_case.walls, None)

        if robot_position[0] != prev_i:
            new_board.board[robot_position[0]] = new_board.board[robot_position[0]].copy()

        new_case = new_board.board[robot_position[0]][robot_position[1]]
        new_board.board[robot_position[0]][robot_position[1]] = Case(new_case.i, new_case.j, new_case.walls, robot)
        # print("...", self.robot_positions, new_board.robot_positions)
        return new_board

    def is_goal_reached(self, robot: int, goal_position: tuple):
        return self.robot_positions[robot] == goal_position

    def display(self, goal_positions, goal: typing.Optional[str] = None):
        displayer.Displayer().display(self.board, goal_positions, goal)

    def is_move_hintable(self, start_i, start_j, direction: int):
        current_walls = self.board[start_i][start_j].walls

        if direction == constants.DIRECTION_DOWN:
            if (start_i == 15) or (constants.WALL_DOWN in current_walls):
                return False
        elif direction == constants.DIRECTION_UP:
            if (start_i == 0) or (constants.WALL_UP in current_walls):
                return False
        elif direction == constants.DIRECTION_RIGHT:
            if (start_j == 15) or (constants.WALL_RIGHT in current_walls):
                return False
        elif direction == constants.DIRECTION_LEFT:
            if (start_j == 0) or (constants.WALL_LEFT in current_walls):
                return False
        return True
