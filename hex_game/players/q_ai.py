import numpy
from hex_game.utils import *


class QPlayer:
    def __init__(self, model):
        self.model = model

    def get_move(self, player: int, board: numpy.ndarray) -> (int, int):
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        """

        size = board.shape[0]

        qval = self.model.predict(get_splitted_board(board, player), batch_size=1)
        action = numpy.argmax(qval)

        move = action // size, action % size
        print("Q AI played at " + str(move))
        return move
