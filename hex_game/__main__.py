from .q_learning import learn
from hex_game.game import Game
from hex_game.players import *
import keras.models

# for early_reward in [False, True]:
# for gamma in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
#     learn(size=5, epochs=250000, gamma=gamma, first_player=False, early_reward=early_reward,
#           save_path="/notebooks/admin/saves", save=True)

learn(size=5, epochs=2000000, gamma=0.9, first_player=True, early_reward=False,
      save_path="/notebooks/admin/saves/tests_2", save=True, load_model_path="",
      initial_epoch=0, initial_epsilon=1)


# model = keras.models.load_model("/notebooks/admin/model.model")
#
# a = HumanPlayer()
# b = QPlayer(model)
# game = Game(size=5, player0=b, player1=a)
# a.init(game)
# game.start()
