from .q_learning import learn
from hex_game.game import Game
from hex_game.players import *
import keras.models

# for gamma in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
#     learn(size=5, epochs=250000, gamma=gamma, first_player=False, early_reward=False, save_path="/notebooks/admin/saves",
#           save=True)

model = keras.models.load_model("/notebooks/admin/model.model")

a = HumanPlayer()
b = QPlayer(model)
game = Game(size=5, player0=a, player1=b)
a.init(game)
game.start()
