from minmax import PlayerMiniMax
from game_handler import GameHandler
from player_human import HumanPlayer
from ai_poisson import PoissonAI

GameHandler(PoissonAI(), HumanPlayer(), size=11)
