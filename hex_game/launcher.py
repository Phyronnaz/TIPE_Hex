from game import Game
from players.human import HumanPlayer
from players.random import RandomPlayer
from players.negamax import NegaMaxPlayer

player0 = NegaMaxPlayer(10000)
player1 = HumanPlayer()

game = Game(size=3, player0=player0, player1=player1)

# player0.init(game)
player1.init(game)

game.start()
