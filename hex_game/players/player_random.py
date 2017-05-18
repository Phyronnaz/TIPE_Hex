import numpy
from hex_game.main import get_random_move
from hex_game.players.player import Player


class RandomPlayer(Player):
    def __init__(self):
        self.name = "Random"

    def get_move(self, board: numpy.ndarray, player: int):
        return get_random_move(board)

    def get_aux_board(self, board: numpy.ndarray, player: int):
        return None
