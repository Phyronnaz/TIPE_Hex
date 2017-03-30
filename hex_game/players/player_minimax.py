import numpy
from hex_game.negamax import get_move_negamax
from hex_game.players.player import Player


class MinimaxPlayer(Player):
    def __init__(self, depth: int = 10000000000):
        self.values = None
        self.set_depth(depth)

    def set_depth(self, depth):
        self.depth = depth
        self.name = "Minimax"

    def get_move(self, board: numpy.ndarray, player: int):
        move, values = get_move_negamax(board, player, self.depth)
        self.values = values
        return move

    def get_aux_board(self, board: numpy.ndarray, player: int):
        return self.values
