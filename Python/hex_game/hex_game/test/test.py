from hex_game.ai_path import PathAI
from hex_game.game_handler import GameHandler
from hex_game.player_human import HumanPlayer

GameHandler(PathAI(), HumanPlayer())