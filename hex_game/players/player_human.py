import numpy

from hex_game.players.player import Player


class HumanPlayer(Player):
    def __init__(self):
        self.move = None
        self.name = "Human"

    def get_move(self, board: numpy.ndarray, player: int):
        return self.move

    def get_aux_board(self, board: numpy.ndarray, player: int):
        return None
