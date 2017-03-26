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

def get_neighbour_matrix():

    return(neighbour)

def floyd_warshall(W):
    n = len(W)
    for k in range (n):
        for i in range(n):
            for j in range (n):
                W[i,j] = min(W[i,j],W[i,k]+W[k,j])




def get_list(U, i, j):
    pass
