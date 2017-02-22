import keras.models
import numpy as np
import tensorflow as tf
from hex_game.main import play_move, can_play_move, init_board, get_random_move
from hex_game.winner_check import check_for_winner, init_winner_matrix_and_counter
from hex_game.q_learning import get_move_q_learning, get_split_board
from hex_game.negamax import get_move_negamax
from hex_game.graphics import debug


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
        self.ended = False

        # Init game
        self.board = init_board(size)
        self.player = 0
        self.winner_matrix, self.winner_c = init_winner_matrix_and_counter(size)
        self.winner = -1

        self.aux_boards = [np.zeros((size, size)), np.zeros((size, size))]

        self.depths = [0, 0]
        self.random_states = [np.random.RandomState(), np.random.RandomState()]

        for i in range(2):
            if players[i][0] == "Minimax":
                self.depths[i] = players[i][1]

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
            config = tf.ConfigProto()
            sess = tf.Session(config=config)
            keras.backend.set_session(sess)
            with sess.graph.as_default():
                model = keras.models.load_model(self.players[self.player][1])

                move = get_move_q_learning(self.board, self.player, model)

                [q_values] = model.predict(np.array([get_split_board(self.board, self.player)]))

            t = q_values.reshape((self.size, self.size))
            if self.player == 1:
                t = t.T
            self.aux_boards[self.player] = t

            self.play_move(move)

    def click(self, x, y):
        if self.players[self.player][0] == "Human":
            return self.play_move((x, y))
