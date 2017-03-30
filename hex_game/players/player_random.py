import numpy
from numpy.random import RandomState
from hex_game.main import get_random_move
from hex_game.players.player import Player


class RandomPlayer(Player):
    def __init__(self, random_state: RandomState = RandomState()):
        self.random_state = random_state
        self.name = "Random"

    def get_move(self, board: numpy.ndarray, player: int):
        return get_random_move(board, self.random_state)

    def get_aux_board(self, board: numpy.ndarray, player: int):
        return None
