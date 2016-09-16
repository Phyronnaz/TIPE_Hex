import numpy as np

from Base.renderer import Renderer
from Base.hex import Hex

h = Hex()


def update():
    move = (np.random.randint(11), np.random.randint(11))
    h.play_move(move, np.random.randint(2) + 1)
    print(h.get_winner())

r = Renderer(update, h)
