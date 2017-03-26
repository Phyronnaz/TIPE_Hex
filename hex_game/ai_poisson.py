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
    while not find_paths(neighbour_matrix):
        neighbour_matrix = get_next_floyd_warshall(neighbour_matrix)
    move  = get_move(get_best_path(find_paths(neighbour_matrix),neighbour_matrix),U)
    return move

def get_neighbour_matrix(poisson_matrix):
    n = len(poisson_matrix)
    poisson_matrix = -poisson_matrix
    neighbour_matrix = numpy.zeros((n ** 2, n ** 2, 2))
    for i in range (n ** 2):
        for j in range (n ** 2):
            neighbour_matrix[i,j,0] = 1000
            neighbour_matrix[i, j, 1] = i*11+j
    for i in range(n):
        for j in range(i + 1, n):
            if poisson_matrix[i , j] != 1:
                neighbour_matrix[11 * i + (j - 1)       , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * i + (j - 1), 11 * i + j, 1] = 11 * i + (j - 1)
                neighbour_matrix[11 * (i - 1) + j       , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i - 1) + j, 11 * i + j, 1] = 11 * (i - 1) + j
                neighbour_matrix[11 * (i + 1) + (j - 1) , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i + 1) + (j - 1), 11 * i + j, 1] = 11 * (i + 1) + (j - 1)
                neighbour_matrix[11 * (i - 1) + (j + 1) , 11 * i + j , 0] = poisson_matrix[i , j]
                neighbour_matrix[11 * (i - 1) + (j + 1), 11 * i + j, 0] = 11 * (i - 1) + (j + 1)
    return(neighbour_matrix)

def get_next_floyd_warshall(W):
    n = len(W)
    for k in range (n):
        for i in range(n):
            for j in range (i,n):
                if W[i, j, 0] > W[i, k, 0] + W[k, j, 0]:
                    W[i, j, 0] = W[i, k, 0] + W[k, j, 0]
                    W[i ,j, 1] = k
                    W[k ,j, 1] = i
    return(W)

def find_paths(neighbour_matrix):
    n = len(neighbour_matrix)
    paths = []
    for i in range (numpy.sqrt(n)):
        for j in range (n - numpy.sqrt(n),n):
            if neighbour_matrix[i ,j, 0] != 10000:
                paths.append([i, j, neighbour_matrix[i, (n - 1) * n + j, 0]])
    return(paths)



def get_best_path(paths_list, neighbour_matrix):
    n = numpy.sqrt(len(neighbour_matrix))
    m = len(paths_list)
    best = paths_list[0]
    for k in range(1, m):
        if paths_list[k][2] < best[2]:
            best = paths_list[k]
    fst , lst = best[0] , best[1]
    j = lst
    path = [lst]
    while j != fst:
        i = neighbour_matrix[fst,j,1]
        path.append(i)
        j = i
    path.append(fst)
    l = len(path)
    final_path = []
    for k in range (n):
        final_path.append((path[k]//n,path[k]%n))
    return(final_path)


def get_move(path, poisson_matrix):
    #refaire la minimisation de l'écart a la moyenne sur la liste du chemin trouvé pour trouver le bon move
    def esperance:
        mini = 0
        return mini
    move = path[0]
    for k in path:
        i, j  = k
    return move


def get_list(U, i, j):
    pass
