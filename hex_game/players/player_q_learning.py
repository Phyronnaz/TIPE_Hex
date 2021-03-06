import keras
import numpy

from hex_game.hex_io import get_pretty_name, get_parameters, get_parameters_dict
from hex_game.main import invert_board
from hex_game.players.player import Player
from hex_game.q_learning import get_move_q_learning, get_features
from hex_game.tf_init import sess


class QLearningPlayer(Player):
    def __init__(self, model_path):
        self.path = model_path
        self.name = get_pretty_name(*get_parameters(model_path))
        self.size = get_parameters_dict(model_path)["size"]

    def get_move(self, board: numpy.ndarray, player: int):
        with sess.graph.as_default():
            model = keras.models.load_model(self.path)
            move = get_move_q_learning(board, player, model)
        return move

    def get_aux_board(self, board: numpy.ndarray, player: int):
        with sess.graph.as_default():
            model = keras.models.load_model(self.path)
            [q_values] = model.predict(numpy.array([get_features(invert_board(board, player))]))
        t = q_values.reshape(board.shape)

        if player == 1:
            t = t.T
            t *= -1
        return t

    def check(self, size):
        return size == self.size
