import numpy

from hex_game.main import get_random_move
from hex_game.poisson import Poisson

NEIGHBORS_1 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]

def get_poisson(board):
    poisson = Poisson(board)
    poisson.iterations(1000)
    U = poisson.U
    print("Poisson Matrix:")
    print(U)
    return get_random_move(board, numpy.random.RandomState())

def get_neighbour_matrix(poisson_matrix):
    n = len(poisson_matrix)
    poisson_matrix = -poisson_matrix
    neighbour_matrix = 10000 * numpy.ones((n ** 2, n ** 2))
    for i in range(n):
        for j in range(i + 1, n):
            if poisson_matrix[i , j] != 1:
                neighbour_matrix[11 * i + (j + 1)       , 11 * i + j] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i + 1) + j       , 11 * i + j] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i + 1) + (j - 1) , 11 * i + j] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i - 1) + (j + 1) , 11 * i + j] = poisson_matrix[i , j]
    return(neighbour_matrix)

def get_next_floyd_warshall(W):
    n = len(W)
    for i in range(n):
        for j in range (i,n):
            W[i, j] = min(W[i, j], W[i, k] + W[k, j])
    return(W)

def get_best_path(W):
    return()





def get_list(U, i, j):
    pass
