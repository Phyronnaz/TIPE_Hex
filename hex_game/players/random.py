import numpy
from hex_game.main   import get_random_move


class RandomPlayer:
    def __init__(self, state=None, verbose=False):
        self.verbose = verbose
        self.state = numpy.random.RandomState() if state is None else state
        self.count = 0

    def get_move(self, player: int, board: numpy.ndarray) -> (int, int):
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        """
        self.count += 1
        if self.verbose:
            print("Random called %s time" % self.count)
        return get_random_move(board, self.state)
