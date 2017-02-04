import keras.models
import numpy as np
from hex_game.main import play_move, can_play_move, init_board, get_random_move
from hex_game.winner_check import check_for_winner, init_winner_matrix_and_counter
from hex_game.q_learning import get_move_q_learning
from hex_game.negamax import get_move_negamax


class Game:
    def __init__(self, size, players):
        """
        Create Game
        :param size: size of the board
        :param players: list of "Name", "Paramater" ("Human", "" or "Minimax", 12 or "Q leaning", model_path)
        """
        # Assign variables
        self.size = size
        self.players = players

        # Init game
        self.board = init_board(size)
        self.player = 0
        self.winner_matrix, self.winner_c = init_winner_matrix_and_counter(size)
        self.winner = -1

        self.aux_boards = [np.zeros((size, size)), np.zeros((size, size))]

        self.models = [None, None]
        self.depths = [0, 0]
        self.random_states = [np.random.RandomState(), np.random.RandomState()]

        for i in range(2):
            if players[i][0] == "Minimax":
                self.depths[i] = players[i][1]
            elif players[i][0] == "Q learning":
                self.models[i] = keras.models.load_model(players[i][1])

    def play_move(self, move):
        if self.winner == -1:
            if can_play_move(self.board, move):
                play_move(self.board, move, self.player)
                self.winner, self.winner_c = check_for_winner(move, self.player, self.winner_matrix, self.winner_c)
                self.player = 1 - self.player
                return move
            else:
                print("Failed to play!")

    def play(self):
        name, _ = self.players[self.player]
        if name == "Human":
            return
        elif name == "Minimax":
            move, values = get_move_negamax(self.board, self.player, self.depths[self.player])
            self.aux_boards[self.player] = values
            self.play_move(move)
        elif name == "Random":
            self.play_move(get_random_move(self.board, self.random_states[self.player]))
        elif name == "Q learning":
            move, q_values = get_move_q_learning(self.board, self.player, self.models[self.player])
            t = q_values.reshape((self.size, self.size))
            self.aux_boards[self.player] = t if self.player == 0 else t.T
            self.play_move(move)

    def click(self, x, y):
        if self.players[self.player][0] == "Human":
            return self.play_move((x, y))
