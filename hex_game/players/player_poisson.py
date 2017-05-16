import numpy
from hex_game.ai_poisson import get_move_poisson, get_poisson
from hex_game.main import invert_board
from hex_game.players.player import Player


class PoissonPlayer(Player):
    def __init__(self):
        self.name = "Poisson"

    def get_move(self, board: numpy.ndarray, player: int):
        move = get_move_poisson(board, player)
        return move

    def get_aux_board(self, board: numpy.ndarray, player: int):
        i_board = invert_board(board, player)
        U = get_poisson(i_board)
        V = 1 + 1 / board.shape[0] - U # type: numpy.ndarray
        return V if player == 0 else -V.T
