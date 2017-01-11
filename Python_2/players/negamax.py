import numpy
from negamax import get_move_negamax


class NegaMaxPlayer:
    def __init__(self, depth: int):
        self.depth = depth

    def get_move(self, player: int, board: numpy.ndarray) -> (int, int):
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        """

        return get_move_negamax(board, player, self.depth)
