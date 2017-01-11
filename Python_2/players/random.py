import numpy
from hex_game import get_move_random


class RandomPlayer:
    def __init__(self, state=None):
        self.state = numpy.random.RandomState() if state is None else state
        self.count = 0

    def get_move(self, player: int, board: numpy.ndarray) -> (int, int):
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        """
        self.count += 1
        print("Random called %s time" % self.count)
        return get_move_random(board, self.state)
