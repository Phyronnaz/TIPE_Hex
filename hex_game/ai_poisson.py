import numpy

from hex_game.main import get_random_move, NEIGHBORS_1
from hex_game.poisson import Poisson


def get_poisson(board):
    poisson = Poisson(board)
    poisson.iterations(1000)
    U = poisson.U
    print("Poisson Matrix:")
    print(U)
    neighbour_matrix = get_neighbour_matrix(U)
    while not find_paths(neighbour_matrix):
        neighbour_matrix = get_next_floyd_warshall(neighbour_matrix)
    move = get_move(get_best_path(find_paths(neighbour_matrix), neighbour_matrix), U)
    return move


def get_neighbour_matrix(poisson_matrix, board, player):
    poisson_matrix += numpy.max(numpy.abs(poisson_matrix))

    # Initialisation of the neighbour matrix
    n = poisson_matrix.shape[0]
    poisson_matrix = -poisson_matrix  # changes the sign of the poisson matrix value to find the least weighted path
    neighbour_matrix = numpy.zeros((n, n, n, n, 2), dtype=object)

    neighbour_matrix[:, :, :, :, 0] = float("inf")
    neighbour_matrix[:, :, :, :, 1] = []

    # Create paths with all linked cells with the cell's poisson value as the weight and the linked cell as the
    # precedent neighbour
    for i in range(n):
        for j in range(i + 1, n):
            if board[i, j] != 1 - player:
                for (k, l) in NEIGHBORS_1:
                    a = i + k
                    b = j + l
                    neighbour_matrix[a, b, i, j, 0] = poisson_matrix[i, j]
                    neighbour_matrix[a, b, i, j, 1] = [(a, b)]

    return neighbour_matrix


def get_next_floyd_warshall(W):
    # Classical Floyd Warshall algorithm with the precedent neighbour kept in memory to rebuild the explored paths
    n = len(W)
    for k in range(n):
        for l in range(n)
            for a in range(n):
                for a in range(n):
                    for i in range (n):
                        for j in range (n):
                            if W[a, b, i, j, 0] > W[a,b,k,l, 0] + W[k,l,i,j, 0] and (k,l) not in W[a,b,k,l,1] and (a,b) not in W[k,l,i,j,1]:
                                W[a,b,i,j, 0] = W[a,b,k,l, 0] + W[k, l,i,j, 0]
                                W[a, b, i,j, 1].append((k,l))
    return W


def find_paths(neighbour_matrix):
    # Explore the cells of the neighbour matrix representing a path from a starting cell to an ending one (to find a
    # complete path)
    n = len(neighbour_matrix)
    paths = []
    for i in range(numpy.sqrt(n)):
        for j in range(n - numpy.sqrt(n), n):
            if neighbour_matrix[i, j, 0] != float("inf"):
                paths.append([i, j, neighbour_matrix[i, (n - 1) * n + j, 0]])
    return paths


def get_best_path(paths_list, neighbour_matrix):
    # Finds the least weighted path among all available paths and returns the right coordinates in the board
    n = numpy.sqrt(len(neighbour_matrix))
    m = len(paths_list)
    best = paths_list[0]
    for k in range(1, m):
        if paths_list[k][2] < best[2]:
            best = paths_list[k]
    fst, lst = best[0], best[1]
    j = lst
    path = [lst]
    while j != fst:
        i = neighbour_matrix[fst, j, 1]
        path.append(i)
        j = i
    path.append(fst)
    l = len(path)
    final_path = []
    for k in range(n):
        final_path.append((path[k] // n, path[k] % n))
    return final_path


def get_move(path, poisson_matrix):
    # Finds the best path by  minimizing the sum of the difference from the average (with poisson matrix)
    # TODO
    def esperance():
        mini = 0
        return mini

    move = path[0]
    for k in path:
        i, j = k
    return move


def get_list(U, i, j):
    pass
