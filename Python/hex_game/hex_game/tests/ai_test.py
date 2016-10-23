import hex_game.hex_game as hex
from hex_game.ai_path import PathAI
from hex_game.renderer import Renderer

renderer = Renderer(debug_text=True)
board = hex.init_board()
for a, (x, y) in PathAI.first_move(board, 0):
    renderer.create_hexagon(x, y, "green", transparent=True)

renderer.start()
