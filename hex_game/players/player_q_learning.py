import keras
import numpy
import tensorflow as tf

from hex_game.hex_io import get_pretty_name, get_parameters, get_parameters_dict
from hex_game.players.player import Player
from hex_game.q_learning import get_move_q_learning, get_features


class QLearningPlayer(Player):
    def __init__(self, model_path):
        self.path = model_path
        self.model = None
        self.name = get_pretty_name(*get_parameters(model_path))
        self.size = get_parameters_dict(model_path)["size"]

    def get_move(self, board: numpy.ndarray, player: int):
        if self.model is None:
            self.model = keras.models.load_model(model_path)
        config = tf.ConfigProto()
        sess = tf.Session(config=config)
        keras.backend.set_session(sess)
        with sess.graph.as_default():
            move = get_move_q_learning(board, player, self.model)
        return move

    def get_aux_board(self, board: numpy.ndarray, player: int):
        [q_values] = self.model.predict(numpy.array([get_features(board, player)]))
        t = q_values.reshape(board.shape)
        if player == 1:
            t = t.T
            t *= -1
        return t

    def check(self, size):
        return size == self.size
