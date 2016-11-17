from minmax import PlayerMiniMax
from game_handler import GameHandler
from player_human import HumanPlayer

GameHandler(PlayerMiniMax(), HumanPlayer(), size=3)