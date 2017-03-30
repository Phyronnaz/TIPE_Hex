import numpy
from hex_game.ai_poisson import get_move_poisson, get_poisson
from hex_game.players.player import Player


class PoissonPlayer(Player):
    def __init__(self):
        self.name = "Poisson"

    def get_move(self, board: numpy.ndarray, player: int):
        move = get_move_poisson(board, player)
        return move

    def get_aux_board(self, board: numpy.ndarray, player: int):
        U = get_poisson(board)
        return 2 - U
