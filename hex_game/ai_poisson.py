from collections import deque

import numpy

from hex_game.graphics import debug
from hex_game.main import get_random_move, NEIGHBORS_1, init_board, is_neighboring, play_move_and_copy, can_play_move
from hex_game.poisson import Poisson


def get_move_poisson(board, player):
    W, P = get_neighbour_and_previous_matrix(board, player)

    while floyd_warshall(W, P):
        pass

    start, end = find_start_end(W)

    path = get_best_path(start, end, P)

    debug.debug_path([k if player == 0 else (k[1], k[0]) for k in path])

    move = get_move(path, board, player)

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


def get_poisson(board):
    m = board.shape[0]

    # Create edges
    B = -numpy.ones((m + 2, m + 2), dtype=int)  # Large board
    B[1:m + 1, 1:m + 1] = board

    # Set edges values
    B[0, :] = 0
    B[-1, :] = 0
    B[:, 0] = 1
    B[:, -1] = 1
    B[0, 0] = -1
    B[-1, -1] = -1
    B[1, -1] = -1
    B[-1, 1] = -1

    poisson = Poisson(B)
    poisson.iterations(1000)
    U = poisson.U
    U += 2
    return U[1:m + 1, 1:m + 1]


def get_neighbour_and_previous_matrix(board, player):
    board = invert_board(board, player)
    U = get_poisson(board)
    # Initialization of the neighbour matrix
    n = U.shape[0]
    W = float("inf") * numpy.ones((n, n, n, n))  # Neighbour matrix
    P = -numpy.ones((n, n, n, n, 2), dtype=int)  # Previous matrix

    # Create paths with all linked cells with the cell's poisson value as the weight and the linked cell as the
    # precedent neighbour
    for i in range(n):
        for j in range(n):
            if board[i, j] != 1:
                for (k, l) in NEIGHBORS_1:
                    a = i + k
                    b = j + l
                    if 0 <= a < n > b >= 0:
                        W[a, b, i, j] = U[i, j]
                        P[a, b, i, j] = (a, b)

    return W, P


def floyd_warshall(W, P):
    # Classical Floyd Warshall algorithm with the precedent neighbour kept in memory to rebuild the explored paths
    n = W.shape[0]
    modified = False
    for a in range(n):
        for b in range(n):
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        for l in range(n):
                            if W[a, b, i, j] > W[a, b, k, l] + W[k, l, i, j]:
                                W[a, b, i, j] = W[a, b, k, l] + W[k, l, i, j]
                                P[a, b, i, j] = (k, l)
                                modified = True
    return modified


def find_start_end(W):
    # Explore the cells of the neighbour matrix representing a path from a starting cell to an ending one (to find a
    # complete path)
    n = W.shape[0]
    min_value = float("inf")
    start, end = None, None
    for i in range(n):
        for j in range(n):
            if min_value > W[0, i, n - 1, j]:
                min_value = W[0, i, n - 1, j]
                start = numpy.array([0, i])
                end = numpy.array([n - 1, j])

    return start, end


def get_best_path(start, end, P):
    n = P.shape[0]

    def aux(pile: deque, start, end):
        middle = P[start[0], start[1], end[0], end[1]]
        if -1 in middle:
            return
        elif is_neighboring(start, end):
            pile.append(start)
            return
        else:
            aux(pile, start, middle)
            pile.append(middle)
            aux(pile, middle, end)

    pile = deque()
    aux(pile, start, end)
    pile.append(end)

    return numpy.array(pile)


def dev_from_avg(t):
    return t - t.mean()


def get_move(path, board, player):
    # Finds the best path by minimizing the sum of the difference from the average (with poisson matrix)
    n = len(path)
    X, Y = path.T
    weights = numpy.zeros((n, n))

    for i in range(n):
        p = path[i]
        if can_play_move(board, p):
            new_board = play_move_and_copy(board, p, 0)
            U = get_poisson(invert_board(new_board, player))
            weights[i] = U[X, Y]

    S = numpy.apply_along_axis(numpy.sum, 0, numpy.apply_along_axis(dev_from_avg, 0, weights))

    w = [board[X, Y] == -1]
    k = numpy.argmin(S[w])

    move = tuple(path[w][k])
    print(move)
    return move
