from player import Player
from hex_game import *


class Game:
    def __init__(self, player0: Player, player1: Player, visual_size: int = 11, board: numpy.ndarray = None):
        self.players = [player0, player1]
        self.board = init_board(visual_size) if board is None else board
        self.winner = -1

    def get_copy(self):
        return Game(self.players[0], self.players[1], board=self.board.copy())

    def get_empty_copy(self):
        return Game(self.players[0], self.players[1], visual_size=self.board.shape[0] - 2)

    def play(self, player: int, check_for_winner: bool = True) -> bool:
        if check_for_winner:
            self.check_for_winner()
        response = self.players[player].play_move(player, self.board)
        message = "" if "message" not in response else response["message"]
        try:
            success = response["success"]
        except ValueError:
            raise Exception("Player must return a success value!")
