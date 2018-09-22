
import typing

import constants
from board import Board
from board_try import BoardTry


class Game:
    _goals = list(constants.Goal)

    def __init__(
        self, board: Board, goal_positions: typing.Dict[constants.Goal, tuple]
    ):
        self._board = board
        self.goal_positions = goal_positions

    def resolve_all(self):
        current_board = self._board
        for goal in self._goals:
            print("Resolving " + str(goal))
            current_board.display(self.goal_positions, goal)
            current_board = self.resolve_goal(
                current_board, goal, self.goal_positions[goal]
            )
            print("")
            print("")
            print("")

    def resolve_goal(
        self, start_board: Board, goal: constants.Goal, goal_position: tuple
    ):
        if goal != constants.Goal.ANY:
            main_robot = constants.GOAL_TO_ROBOT[goal]
            robots = sorted(constants.Robot, key=lambda k: 0 if k == main_robot else 1)
        else:
            robots = list(constants.Robot)

        current_tries = [BoardTry(start_board, None, None)]
        nb_turns = 0
        seen_positions = set()
        for nb_turns in range(constants.MAX_TURNS):
            print(
                "...move {}, {} possibilities".format(
                    str(nb_turns + 2), len(current_tries)
                )
            )
            new_tries = []
            for current_try in current_tries:
                successful_try = current_try.gen_leafs(
                    goal_position, goal, robots, seen_positions
                )
                if successful_try:
                    moves = [successful_try]
                    ancestor = successful_try
                    while ancestor.parent:
                        moves.append(ancestor.parent)
                        ancestor = ancestor.parent
                    for elem in reversed(moves):
                        elem.result_board.display(self.goal_positions, goal)
                    # successful_try.result_board.display(self.goal_positions)
                    print("...resolved in {} turns".format(nb_turns + 2))
                    return successful_try.result_board
                new_tries.extend(current_try.leafs)
            current_tries = new_tries
        raise ValueError("No solution found in {}".format(nb_turns + 2))
