import constants
from board import Board
from board_try import BoardTry


class Game:
    _goals = list(constants.Goal)

    def __init__(self, board: Board):
        self._board = board

    def resolve_all(self):
        current_board = self._board
        for goal in self._goals:
            print("Resolving " + str(goal))
            current_board.display(goal)
            current_board, nb_turns = self.resolve_goal(current_board, goal)
            print("...resolved in {} turns".format(nb_turns + 1))
            print("")
            print("")
            print("")

    def resolve_goal(self, start_board: Board, goal: constants.Goal):
        other_robots = []
        try:
            main_robot = constants.GOAL_TO_ROBOT[goal]
            other_robots = [x for x in list(constants.Robot) if x != main_robot]
        except KeyError:
            main_robot, *other_robots = list(constants.Robot)

        current_tries = [BoardTry(start_board, None, None)]
        nb_turns = 0
        for nb_turns in range(constants.MAX_TURNS):
            print(
                "...move {}, {} possibilities".format(
                    str(nb_turns + 1), len(current_tries)
                )
            )
            new_tries = []
            for current_try in current_tries:
                successful_try = current_try.gen_leafs(goal, main_robot, other_robots)
                if successful_try:
                    successful_try.result_board.display()
                    return successful_try.result_board, nb_turns
                new_tries.extend(current_try.leafs)
            current_tries = new_tries
        raise ValueError("No solution found in {}".format(nb_turns + 1))
