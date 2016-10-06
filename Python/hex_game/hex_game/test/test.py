from hex_game.ai_path import PathAI
from hex_game.game_handler import GameHandler
from hex_game.player_human import HumanPlayer

# Human vs Human
# GameHandler(NeuralNetworkAI(), Player())

# Player (random) vs Human
# GameHandler(Player())

# AI vs Player
GameHandler(HumanPlayer(), PathAI())
