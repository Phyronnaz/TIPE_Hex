from minmax import PlayerMiniMax
from game_handler import GameHandler
from player_human import HumanPlayer
from ai_poisson import PoissonAI
from player import Player
from alphabeta import PlayerAlphaBeta

GameHandler(PoissonAI(), HumanPlayer(), visual_size=11)
