import numpy as np

from hex_game.hex_game import HexGame
from hex_game.renderer import Renderer

h = HexGame(None)
h.play_move()

def update():
    w = h.get_winner()
    if w == 0:
        c = False
        while not c:
            move = (np.random.randint(11), np.random.randint(11))
            c = h.play_move(move, np.random.randint(2) + 1)
    else:
        print(w)

r = Renderer(update, h)
