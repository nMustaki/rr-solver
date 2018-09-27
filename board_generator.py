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

    # robot_positions_lst = random.choices(board, k=4)
    # goal_positions_lst = random.choices(board, k=17)

    # pypy doesn't know random.choices
    robot_positions_lst = []
    while len(robot_positions_lst) < 4:
        pos = random.choice(board)
        if pos not in robot_positions_lst:
            robot_positions_lst.append(pos)
    goal_positions_lst = []
    while len(goal_positions_lst) < 17:
        pos = random.choice(board)
        if pos not in goal_positions_lst:
            goal_positions_lst.append(pos)

    goal_positions_dict = dict(zip(constants.GOALS, goal_positions_lst))
    return robot_positions_lst, goal_positions_dict


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
    board = Board(robot_positions, [[]] * 16)

    close_set = set((constants.WALL_UP, constants.WALL_LEFT))
    for i in range(16):
        board.board[i] = [[]] * 16

        for j in range(16):
            robot, walls = None, set()

            if (7 <= i < 9) and (7 <= j < 9):
                board.board[i][j] = Case(i, j, constants.WALLS, None)
            else:
                if i == 0 or constants.WALL_DOWN in board.board[i - 1][j].walls:
                    walls.add(constants.WALL_UP)
                if j == 0 or constants.WALL_RIGHT in board.board[i][j - 1].walls:
                    walls.add(constants.WALL_LEFT)
                if i == 15:
                    walls.add(constants.WALL_DOWN)
                if j == 15:
                    walls.add(constants.WALL_RIGHT)

                if not close_set.issubset(walls) and random.random() < 0.12:
                    if i in (0, 15):
                        if not (
                            j > 0
                            and constants.WALL_RIGHT in board.board[i][j - 1].walls
                        ):
                            walls.add(constants.WALL_RIGHT)
                    elif j in (0, 15):
                        if not (
                            i > 0 and constants.WALL_DOWN in board.board[i - 1][j].walls
                        ):
                            walls.add(constants.WALL_DOWN)
                    else:
                        walls = walls.union(constants.CASE_WALLS)

                try:
                    robot = constants.ROBOTS[robot_positions.index((i, j))]
                except ValueError:
                    pass
                board.board[i][j] = Case(i, j, set(walls), robot)
    return board, goal_positions
