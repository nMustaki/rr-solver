import random
import sys
import board_generator
from game import Game


if __name__ == "__main__":
    try:
        seed = int(sys.argv[1])
    except IndexError:
        seed = None
    random.seed(seed)

    board, goal_positions = board_generator.generate()
    game = Game(board, goal_positions)
    game.resolve_all()
