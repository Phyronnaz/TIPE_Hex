import numpy
# noinspection PyUnresolvedReferences
from hex_game.floyd_warshall.floyd_warshall import floyd_warshall

from hex_game.graphics import debug
from hex_game.main import is_neighboring, get_common_neighbors, get_neighbors_1, get_neighbors_2, add_edges, \
    invert_path, invert_board
from hex_game.poisson import Poisson

poisson_dict = {}


def get_move_poisson(board, player):
    paths = [get_path(board, p) for p in [0, 1]]

    # paths_values = [None, None]
    # for p in [0, 1]:
    #     X, Y = paths[p].T
    #     i_board = invert_board(board, p)
    #     paths_values[p] = get_poisson(i_board)[X, Y]
    #
    # best = numpy.argmax([sum(paths_values[p]) for p in [0, 1]])
    # i_board = invert_board(board, best)
    # move = get_move(paths[best], i_board)
    #
    # return invert_move(move, best)

    real_paths = [invert_path(paths[p], p) for p in [0, 1]]

    debug.debug_path(real_paths[0], id=0, player=player)
    debug.debug_path(real_paths[1], id=1, player=player)

    return [k for k in real_paths[0] if k in real_paths[1]][0]


def get_path(board, player):
    i_board = add_edges(invert_board(board, player), 1)

    W, P = get_weights_and_precedents_matrix(i_board)

    # Floyd
    while floyd_warshall(W, P):
        pass

    # Find path
    start, end = find_start_end(W)
    path = find_path(start, end, P, i_board)

    # Remove edges
    path = [(x - 1, y - 1) for (x, y) in path]

    return path


def get_poisson(board):
    key = board.tostring()
    if key not in poisson_dict:
        n = board.shape[0]

        # Create edges
        B = add_edges(board, 1)

        scales = numpy.ones((n + 2, n + 2))
        c = 1  # How much edges are used in poisson
        scales[0, :] = c
        scales[-1, :] = c
        scales[:, 0] = c
        scales[:, -1] = c
        scales[0, 0] = c
        scales[-1, -1] = c
        scales[1, -1] = c
        scales[-1, 1] = c

        poisson = Poisson(B, scales)
        poisson.process()
        U = poisson.U
        U += 1 + 1 / n

        U = U[1:n + 1, 1:n + 1]
        U.flags.writeable = False

        poisson_dict[key] = U

    return poisson_dict[key]


def get_weights_and_precedents_matrix(board):
    n = board.shape[0]

    U = get_poisson(board)

    # Initialization of the neighbour matrix
    W = float("inf") * numpy.ones((n, n, n, n))  # Neighbour matrix
    P = -numpy.ones((n, n, n, n, 2), dtype=int)  # Previous matrix

    # Create paths with all linked cells with the cell's poisson value as the weight and the linked cell as the
    # precedent neighbour
    for i in range(n):
        for j in range(n):
            if board[i, j] != 1:  # If it is not an enemy tile
                for (a, b) in get_neighbors_1((i, j), board) + get_neighbors_2((i, j), board):
                    if board[a, b] != 1:
                        W[a, b, i, j] = U[i, j]
                        P[a, b, i, j] = [a, b]

    return W, P


def find_start_end(W):
    """
    Search the best path
    :param W: weights matrix
    :return: (start_x, start_y), (end_x, end_y)
    """
    n = W.shape[0]
    min_value = float("inf")
    start, end = None, None

    for i in range(n):
        for j in range(n):
            if min_value > W[0, i, n - 1, j]:
                min_value = W[0, i, n - 1, j]
                start = (0, i)
                end = (n - 1, j)

    return start, end


def find_path(start, end, P, board):
    """
    Find the path between start and end
    :param start: (int, int) 
    :param end: (int, int)
    :param P: precedents matrix
    :param board: board
    :return: np.ndarray
    """
    U = get_poisson(board)

    def aux(pile, start, end):
        """
        Recursive reconstruction of the path from start to end (excluded)
        :param pile: pile
        :param start: (int, int)
        :param end: (int, int)
        """
        middle = tuple(P[start[0], start[1], end[0], end[1]])

        if middle == (-1, -1):
            debug.debug_play_text("Error rebuilding path: unknown precedent")
        elif start == end:
            debug.debug_play_text("Error rebuilding path: start = end")
        elif is_neighboring(start, end, distance=1):
            pile.append(start)
        elif is_neighboring(start, end, distance=2):
            pile.append(start)
            l = get_common_neighbors(start, end, board)
            best = l[numpy.argmin([U[k] for k in l])]
            pile.append(best)
        else:
            aux(pile, start, middle)
            pile.append(middle)
            aux(pile, middle, end)

    pile = []
    aux(pile, start, end)
    pile.append(end)

    return numpy.array(pile)


def get_move(path, board):
    """
    Get move to play from path
    :param path: tuple list
    :param board: board
    :return: (int, int)
    """
    U = get_poisson(board)

    X, Y = path.T
    i = numpy.argmax(U[X, Y])

    return X[i], Y[i]
