import numpy

from hex_game.main import get_random_move
from hex_game.poisson import Poisson


def get_poisson(board):
    poisson = Poisson(board)
    poisson.iterations(1000)
    U = poisson.U
    print("Poisson Matrix:")
    print(U)
    return get_random_move(board, numpy.random.RandomState())

def get_list(U, i, j):
    pass
