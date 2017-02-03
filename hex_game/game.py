# import keras.models
import numpy as np
from hex_game.main import play_move, can_play_move, init_board, get_random_move
from hex_game.winner_check import check_for_winner, init_winner_matrix_and_counter
from q_learning import get_move_q_learning
from negamax import get_move_negamax


class Game:
    def __init__(self, size, players, display_Q):
        """
        Create Game
        :param size: size of the board
        :param players: list of "Name", "Paramater" ("Human", "" or "Minimax", 12 or "Q leaning", model_path)
        :param display_Q: function display_ai(player, q_values)
        """
        # Assign variables
        self.size = size
        self.players = players
        self.display_Q = display_Q

        # Init game
        self.board = init_board(size)
        self.player = 0
        self.winner_matrix, self.winner_c = init_winner_matrix_and_counter(size)
        self.winner = -1

        a, b = players[0]
        c, d = players[1]
        self.models = [None, None]

        if a == "Q learning":
            self.models[0] = keras.models.load_model(b)
        if c == "Q learning":
            self.models[0] = keras.models.load_model(c)

    def play_move(self, move):
        if self.winner == -1:
            if can_play_move(self.board, move):
                play_move(self.board, move, self.player)
                self.winner, self.winner_c = check_for_winner(move, self.player, self.winner_matrix, self.winner_c)
                self.player = 1 - self.player
                return move
        return None

    def play(self):
        p, q = self.players[self.player]
        if p == "Human":
            return None
        elif p == "Minimax":
            return self.play_move(get_move_negamax(self.board, self.player, q))
        elif p == "Random":
            return self.play_move(get_random_move(self.board, np.random.RandomState()))
        elif p == "Q learning":
            move, _, _, q_val = get_move_q_learning(self.board, self.player, self.models[self.player])
            self.display_Q(self.player, q_val.reshape((self.size, self.size)))
            return self.play_move(move)
        return None

    def click(self, x, y):
        if self.players[self.player][0] == "Human":
            return self.play_move((x, y))
