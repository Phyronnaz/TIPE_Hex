from collections import deque

import numpy

from hex_game.graphics import debug
from hex_game.main import get_random_move, NEIGHBORS_1, init_board, is_neighboring, play_move_and_copy, can_play_move, \
    NEIGHBORS_2, get_common_neighbours, get_neighbors_1, get_neighbors_2
from hex_game.poisson import Poisson
from hex_game.floyd_warshall.floyd_warshall import floyd_warshall


def get_move_poisson(board, player):
    i_board = invert_board(board, player)
    W, P = get_neighbour_and_previous_matrix(i_board)

    while floyd_warshall(W, P):
        pass

    start, end = find_start_end(W)

    path = get_best_path(start, end, P, i_board)

    debug.debug_path([k if player == 0 else (k[1], k[0]) for k in path])

    move = get_move(path, i_board)

    if player == 1:
        move = (move[1], move[0])

    return move


def invert_board(board, player):
    board = board.copy()

    if player == 1:
        board = board.T
        p0 = board == 0
        p1 = board == 1
        board[p0] = 1
        board[p1] = 0

    return board


def get_poisson(board, iterations=1000):
    n = board.shape[0]

    # Create edges
    B = -numpy.ones((n + 2, n + 2), dtype=int)  # Large board
    B[1:n + 1, 1:n + 1] = board

    # Set edges values
    B[0, :] = 0
    B[-1, :] = 0
    B[:, 0] = 1
    B[:, -1] = 1
    B[0, 0] = -1
    B[-1, -1] = -1
    B[1, -1] = -1
    B[-1, 1] = -1

    scales = numpy.ones((n + 2, n + 2))
    c = 1
    scales[0, :] = c
    scales[-1, :] = c
    scales[:, 0] = c
    scales[:, -1] = c
    scales[0, 0] = c
    scales[-1, -1] = c
    scales[1, -1] = c
    scales[-1, 1] = c

    poisson = Poisson(B, scales)
    poisson.iterations(iterations)
    U = poisson.U
    U += 2
    return U[1:n + 1, 1:n + 1]


def get_neighbour_and_previous_matrix(board):
    U = get_poisson(board)

    U[U == 1] = 0.1

    # Initialization of the neighbour matrix
    n = board.shape[0]
    W = float("inf") * numpy.ones((n, n, n, n))  # Neighbour matrix
    P = -numpy.ones((n, n, n, n, 2), dtype=int)  # Previous matrix

    # Create paths with all linked cells with the cell's poisson value as the weight and the linked cell as the
    # precedent neighbour
    for i in range(n):
        for j in range(n):
            if board[i, j] != 1:
                for (a, b) in get_neighbors_1((i, j), n) + get_neighbors_2((i, j), board):
                    if board[a, b] != 1:
                        W[a, b, i, j] = U[i, j]
                        P[a, b, i, j] = [a, b]

    return W, P


# def floyd_warshall(W, P):
#     # Classical Floyd Warshall algorithm with the precedent neighbour kept in memory to rebuild the explored paths
#     n = W.shape[0]
#     modified = False
#     for a in range(n):
#         for b in range(n):
#             for i in range(n):
#                 for j in range(n):
#                     for k in range(n):
#                         for l in range(n):
#                             if W[a, b, i, j] > W[a, b, k, l] + W[k, l, i, j]:
#                                 W[a, b, i, j] = W[a, b, k, l] + W[k, l, i, j]
#                                 P[a, b, i, j] = (k, l)
#                                 modified = True
#     return modified


def find_start_end(W):
    # Explore the cells of the neighbour matrix representing a path from a starting cell to an ending one (to find a
    # complete path)
    n = W.shape[0]
    min_value = float("inf")
    start, end = None, None
    print(W[0, :, n - 1, :])
    for i in range(n):
        for j in range(n):
            if min_value > W[0, i, n - 1, j]:
                min_value = W[0, i, n - 1, j]
                start = numpy.array([0, i])
                end = numpy.array([n - 1, j])

    return start, end


def get_best_path(start, end, P, board):
    U = get_poisson(board)
    n = board.shape[0]

    def aux(pile: deque, start, end):
        middle = P[start[0], start[1], end[0], end[1]]
        if -1 in middle:
            return
        elif is_neighboring(start, end, 1):
            pile.append(start)
            return
        elif is_neighboring(start, end, 2):
            pile.append(start)
            l = [k for k in get_common_neighbours(start, end, n) if board[k] != 1]
            pile.append(l[numpy.argmin([U[k] for k in l])])
            return
        else:
            aux(pile, start, middle)
            pile.append(middle)
            aux(pile, middle, end)

    pile = deque()
    aux(pile, start, end)
    pile.append(end)

    return numpy.array(pile)


def get_move(path, board):
    # Finds the best path by minimizing the sum of the difference from the average (with poisson matrix)
    n = len(path)
    X, Y = path.T

    U = get_poisson(board)
    i = numpy.argmax(U[X, Y])
    return X[i], Y[i]
