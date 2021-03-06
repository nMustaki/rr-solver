import random

import constants
from case import Case
from board import Board


def _gen_elems_positions():
    board = [
        (i, j)
        for i in range(16)
        for j in range(16)
        if not ((7 <= i < 9) and (7 <= j < 9))
    ]

    robot_positions_lst = random.choices(board, k=4)
    goal_positions_lst = random.choices(board, k=17)

    robot_positions_dict = dict(zip(list(constants.Robot), robot_positions_lst))
    goal_positions_dict = dict(zip(list(constants.Goal), goal_positions_lst))
    return robot_positions_dict, goal_positions_dict


def generate():
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X . . X X X X X X X
    # X X X X X X X . . X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X
    # X X X X X X X X X X X X X X X X

    robot_positions, goal_positions = _gen_elems_positions()
    board = Board(robot_positions, goal_positions)

    close_set = set((constants.Wall.UP, constants.Wall.LEFT))
    for i in range(16):
        board.board[i] = [[]] * 16

        for j in range(16):
            robot, goal, walls = None, None, set()

            if (7 <= i < 9) and (7 <= j < 9):
                board.board[i][j] = Case(i, j, None, None, list(constants.Wall), None)
            else:
                if i == 0 or constants.Wall.DOWN in board.board[i - 1][j].walls:
                    walls.add(constants.Wall.UP)
                if j == 0 or constants.Wall.RIGHT in board.board[i][j - 1].walls:
                    walls.add(constants.Wall.LEFT)
                if i == 15:
                    walls.add(constants.Wall.DOWN)
                if j == 15:
                    walls.add(constants.Wall.RIGHT)

                if not close_set.issubset(walls) and random.random() < 0.12:
                    if i in (0, 15):
                        if not (
                            j > 0
                            and constants.Wall.RIGHT in board.board[i][j - 1].walls
                        ):
                            walls.add(constants.Wall.RIGHT)
                    elif j in (0, 15):
                        if not (
                            i > 0 and constants.Wall.DOWN in board.board[i - 1][j].walls
                        ):
                            walls.add(constants.Wall.DOWN)
                    else:
                        walls = walls.union(constants.CASE_WALLS)

                try:
                    robot = list(constants.Robot)[
                        list(robot_positions.values()).index((i, j))
                    ]
                except ValueError:
                    pass
                try:
                    goal = list(constants.Goal)[
                        list(goal_positions.values()).index((i, j))
                    ]
                except ValueError:
                    pass
                board.board[i][j] = Case(i, j, goal, None, set(walls), robot)
    return board
