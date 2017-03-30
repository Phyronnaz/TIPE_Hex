from hex_game.graphics import debug
from hex_game.main import play_move, can_play_move, init_board
from hex_game.players.player import Player
from hex_game.winner_check import check_for_winner, init_winner_matrix_and_counter


class Game:
    def __init__(self, size, players):
        """
        Create Game
        :param size: size of the board
        """
        # Assign variables
        self.size = size
        self.players = players  # type: Player,Player
        self.ended = False

        # Init game
        self.board = init_board(size)
        self.player = 0
        self.winner_matrix, self.winner_c = init_winner_matrix_and_counter(size)
        self.winner = -1

    def play_move(self, move):
        if self.winner == -1:
            if can_play_move(self.board, move):
                play_move(self.board, move, self.player)
                self.winner, self.winner_c = check_for_winner(move, self.player, self.winner_matrix, self.winner_c)
                self.player = 1 - self.player
            else:
                debug.debug_play("Failed to play!")

        if self.winner != -1 and not self.ended:
            self.ended = True
            debug.debug_play("Winner: Player %s" % self.winner)

    def play(self):
        move = self.players[self.player].get_move(self.board, self.player)
        self.play_move(move)

    def click(self, x, y):
        if self.players[self.player][0] == "Human":
            return self.play_move((x, y))
