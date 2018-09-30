
import typing
import datetime

import constants
from board import Board
from board_try import BoardTry


class Game:
    _goals = constants.GOALS

    def __init__(self, board: Board, goal_positions: typing.Dict[str, tuple]):
        self._board = board
        self.goal_positions = goal_positions

    def resolve_all(self):
        current_board = self._board
        start_time = datetime.datetime.now()
        for goal in self._goals:
            print("Resolving", str(goal), self.goal_positions[goal])
            current_board.display(self.goal_positions, goal)
            current_board = self.resolve_goal(current_board, goal, self.goal_positions[goal])
            print("")
            print("")
            print("")
        print(datetime.datetime.now() - start_time)

    def resolve_goal(self, start_board: Board, goal, goal_position: tuple):
        if goal != constants.GOAL_ANY:
            main_robot = constants.GOAL_TO_ROBOT[goal]
            robots = sorted(constants.ROBOTS, key=lambda k: 0 if k == main_robot else 1)
        else:
            robots = constants.ROBOTS

        branches = [[BoardTry(start_board, None, None)]]
        fast_branches = []
        hint_positions = self._find_hint_positions(branches[0][0], goal_position)
        nb_turns = 0
        seen_positions = set()
        for nb_turns in range(constants.MAX_TURNS):
            print(
                "move {}, at most {:,} moves to investigate".format(
                    nb_turns + 1,
                    sum([len(branch) for branch in branches]) + sum([len(branch) for branch in fast_branches]),
                )
            )
            new_branches = []
            new_fast_branches = []
            nb_leaves = 0

            for branch in fast_branches:
                for leaf in branch:
                    if (nb_leaves % 100000) == 0:
                        print("...{:,} moves: {} (fast)".format(nb_leaves, datetime.datetime.now()))
                        nb_leaves += 1

                    successful_try, leaves, fast_leaves = leaf.gen_leaves(
                        goal_position, goal, robots, seen_positions, hint_positions
                    )
                    if successful_try:
                        return self._display_successful(nb_turns, successful_try, goal)

                    new_branches.append(leaves)
                    new_fast_branches.append(fast_leaves)
            print("......{:,} fast leaves investigated".format(nb_leaves))

            tmp_nb_leaves = nb_leaves
            for branch in branches:
                for leaf in branch:
                    if (nb_leaves % 10000) == 0:
                        print("...{:,} moves: {}".format(nb_leaves, datetime.datetime.now()))
                    nb_leaves += 1

                    successful_try, leaves, fast_leaves = leaf.gen_leaves(
                        goal_position, goal, robots, seen_positions, hint_positions
                    )
                    if successful_try:
                        return self._display_successful(nb_turns, successful_try, goal)

                    new_branches.append(leaves)
                    new_fast_branches.append(fast_leaves)
            print("......{:,} leaves investigated".format(nb_leaves - tmp_nb_leaves))

            branches = new_branches
            fast_branches = new_fast_branches

        raise ValueError("No solution found in {} turns".format(nb_turns + 1))

    def _display_successful(self, nb_turns, successful_try, goal):
        moves = [successful_try]
        ancestor = successful_try
        while ancestor.parent:
            if ancestor.parent.parent:
                moves.append(ancestor.parent)
            ancestor = ancestor.parent

        prev_elem = ancestor
        for elem in reversed(moves):
            for robot in constants.ROBOTS:
                if elem.result_board.robot_positions[robot] != prev_elem.result_board.robot_positions[robot]:
                    print(
                        "Moving {} robot to {}".format(
                            constants.ROBOT_TO_COLORS[robot], elem.result_board.robot_positions[robot]
                        )
                    )
            elem.result_board.display(self.goal_positions, goal)
            prev_elem = elem
        print("...resolved in {} turns".format(nb_turns + 1))
        return successful_try.result_board

    def _find_hint_positions(self, root_try, goal_position):
        min_i, max_i, min_j, max_j = (goal_position[0], goal_position[0], goal_position[1], goal_position[1])

        # Try to go up as much as possible
        while min_i > 0 and root_try.root_board.is_move_hintable(min_i, goal_position[1], constants.DIRECTION_UP):
            min_i -= 1
        while max_i < 15 and root_try.root_board.is_move_hintable(max_i, goal_position[1], constants.DIRECTION_DOWN):
            max_i += 1
        while min_j > 0 and root_try.root_board.is_move_hintable(goal_position[0], min_j, constants.DIRECTION_LEFT):
            min_j -= 1
        while max_j < 15 and root_try.root_board.is_move_hintable(goal_position[0], max_j, constants.DIRECTION_RIGHT):
            max_j += 1
        return (min_i, max_i), (min_j, max_j)
