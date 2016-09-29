from hex_game.ai_neural_network import NeuralNetworkAI
from hex_game.game_handler import GameHandler
from hex_game.player import Player

# Human vs Human
# GameHandler(NeuralNetworkAI(), Player())

# Player (random) vs Human
# GameHandler(Player())

# AI vs Player
GameHandler(NeuralNetworkAI(), Player())
