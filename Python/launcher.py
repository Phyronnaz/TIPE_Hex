from hex_game import GameHandler, HumanPlayer
from minmax import PlayerMiniMax

GameHandler(HumanPlayer(), PlayerMiniMax(), size=3)