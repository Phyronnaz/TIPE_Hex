from .q_learning import learn
from hex_game.game import Game
from hex_game.players import *

for gamma in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    learn(size=5, epochs=250000, gamma=gamma, first_player=0, early_reward=False, save_path="/notebooks/admin/saves",
          save=True)

# a = RandomPlayer()
# b = QPlayer(model)
# player0, player1 = (a, b) if player == 1 else (b, a)
# game = Game(size=size, player0=player0, player1=player1)
# game.start()
