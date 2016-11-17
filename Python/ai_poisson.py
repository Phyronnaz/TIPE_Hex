from player import Player
from poisson import Poisson
from hex_game import *
import numpy


class PoissonAI(Player):
    def init(self, renderer):
        pass

    def play_move(self, player: int, board: numpy.ndarray) -> int:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
        move = moves[numpy.argmax(
            [[-1, 1][player] * self.get_norme(play_move_copy(board, moves[i][0], moves[i][1], player)) for i in
             range(len(moves))])]
        return play_move(board, move[0], move[1], player)

    @staticmethod
    def get_norme(board):
        poisson = Poisson(board)
        poisson.iterations(50)
        return poisson.norme()
