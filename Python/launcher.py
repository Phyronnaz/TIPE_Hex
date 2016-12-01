from minmax import PlayerMiniMax
from game_handler import GameHandler
from player_human import HumanPlayer
from ai_poisson import PoissonAI
from player import Player
from alphabeta import PlayerAlphaBeta


GameHandler(HumanPlayer(), PlayerAlphaBeta(), visual_size=3, rate=50)