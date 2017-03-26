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
    neighbour_matrix = get_neighbour_matrix(U)
    while find_paths(neighbour_matrix) = []:
        neighbour_matrix = get_next_floyd_warshall(neighbour_matrix)

    return get_random_move(board, numpy.random.RandomState())

def get_neighbour_matrix(poisson_matrix):
    n = len(poisson_matrix)
    poisson_matrix = -poisson_matrix
    neighbour_matrix = numpy.zeros((n ** 2, n ** 2,3))
    for i in range (n ** 2):
        for j in range (n ** 2):
            neighbour_matrix[i,j,0] = 1000
            neighbour_matrix[i, j, 1] = i
            neighbour_matrix[i, j, 2] = j
    for i in range(n):
        for j in range(i + 1, n):
            if poisson_matrix[i , j] != 1:
                neighbour_matrix[11 * i + (j - 1)       , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * i + (j - 1), 11 * i + j, 1] = i
                neighbour_matrix[11 * i + (j - 1), 11 * i + j, 2] = j - 1
                neighbour_matrix[11 * (i - 1) + j       , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i - 1) + j, 11 * i + j, 1] = i - 1
                neighbour_matrix[11 * (i - 1) + j, 11 * i + j, 2] = j
                neighbour_matrix[11 * (i + 1) + (j - 1) , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i + 1) + (j - 1), 11 * i + j, 1] = i + 1
                neighbour_matrix[11 * (i + 1) + (j - 1), 11 * i + j, 2] = j - 1
                neighbour_matrix[11 * (i - 1) + (j + 1) , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i - 1) + (j + 1), 11 * i + j, 0] = i - 1
                neighbour_matrix[11 * (i - 1) + (j + 1), 11 * i + j, 0] = j + 1
    return(neighbour_matrix)

def get_next_floyd_warshall(W):
    n = len(W)
    for i in range(n):
        for j in range (i,n):
            W[i, j] = min(W[i, j], W[i, k] + W[k, j])
    return(W)

def find_paths(neighbour_matrix):
    n = numpy.sqrt(len(neighbour_matrix))
    paths = []
    for i in range (n):
        for j in range (n):
            if neighbour_matrix[i , (n - 1) * n + j] != 10000:
                paths.append(([0 , i] , [n-1 , j] , neighbour_matrix[i , (n - 1) * n + j]))
    return(paths)



def get_best_path(paths_list):
    n = len(paths_list)
    best = paths_list[0]
    for k in range(0,n):
        if paths_list[k][3] < best[3]:
            best = paths_list[k][3]
    return(best)


def get_move(path):


def get_list(U, i, j):
    pass
