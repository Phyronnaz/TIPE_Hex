############################
# Fichier de l'heuristique #
############################



import numpy as np
# noinspection PyUnresolvedReferences
from hex_game.floyd_warshall.floyd_warshall import floyd_warshall

from hex_game.graphics import debug
from hex_game.main import is_neighboring, get_common_neighbors, get_neighbors_1, get_neighbors_2, add_edges, \
    invert_path, invert_board, play_move_and_copy
from hex_game.poisson import Poisson

poisson_dict = {}


def get_move_poisson(board : np.ndarray, player: int, debug_path=True) -> (int, int):
    """
    Return heuristic move
    :param board: board
    :param player: player
    :param debug_path: debug path?
    :return: 
    """
    paths = [get_path(board, p) for p in [0, 1]]

    real_paths = [invert_path(paths[p], p) for p in [0, 1]]

    if debug_path:
        debug.debug_path(real_paths[0], id=0, player=player)
        debug.debug_path(real_paths[1], id=1, player=player)

    valid_paths = [validate_path(c, board) for c in real_paths]
    expanded_paths = [expand_path(c, board) for c in real_paths]

    valid_expanded_paths = [validate_path(c, board) for c in expanded_paths]

    l = [k for k in valid_expanded_paths[0] if k in valid_expanded_paths[1] and board[k] == -1]

    c = [1, -1][player]

    i = np.argmax([c * score(invert_board(play_move_and_copy(board, k, player), player), *valid_paths) for k in l])

    return l[i]


def validate_path(path : [(int, int)], board : np.ndarray) -> [(int, int)]:
    """
    Return path without invalid tiles
    :param path: path
    :param board: board
    :return: path
    """
    n = board.shape[0]
    return [(a, b) for (a, b) in path if 0 <= a < n > b >= 0]


def score(board : np.ndarray, path : [(int, int)], enemy_path:[(int, int)]) -> float:
    """
    Return the score (weigths of enemy path + weigths of player path)
    :param board: board
    :param path: player path
    :param enemy_path: enenmy path
    :return: score
    """
    U = get_poisson(board)

    [A, B] = np.array(path).T
    [C, D] = np.array(enemy_path).T

    return sum(U[C, D]) + sum(U[A, B])


def expand_path(path : [(int, int)], board : np.ndarray) -> [(int, int)]:
    """
    Add NEIGHBORS_2 to path path 
    :param path: path
    :param board: board
    :return: path with extra tiles
    """
    l = []
    for i in range(len(path) - 1):
        l.append(path[i])
        if not is_neighboring(path[i], path[i + 1], distance=1, board=board):
            l += get_common_neighbors(path[i], path[i + 1], board)
    l.append(path[-1])
    return l


def get_path(board : np.ndarray, player : int) -> [(int, int)]:
    """
    Get the path of player player on board board
    :param board: board
    :param player: player
    :return: path
    """
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


def get_poisson(board : np.ndarray) -> np.ndarray:
    """
    Calculate poisson weights matrix
    :param board: board
    :return: poisson + 1 + 1/n
    """
    key = board.tostring()
    if key not in poisson_dict:
        n = board.shape[0]

        # Create edges
        B = add_edges(board, 1)

        scales = np.ones((n + 2, n + 2))
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


def get_weights_and_precedents_matrix(board: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Initialize weights and precedents matrix
    :param board: board
    :return: weights, precedents
    """

    n = board.shape[0]

    U = get_poisson(board)

    # Initialization of the neighbour matrix
    W = float("inf") * np.ones((n, n, n, n))  # Neighbour matrix
    P = -np.ones((n, n, n, n, 2), dtype=int)  # Previous matrix

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


def find_start_end(W : np.ndarray) -> ((int, int), (int, int)):
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


def find_path(start : (int, int), end : (int, int), P : np.ndarray, board : np.ndarray) -> np.ndarray:
    """
    Find the path between start and end
    :param start: start position
    :param end: end position
    :param P: precedents matrix
    :param board: board
    :return: path
    """

    def aux(pile, start, end):
        """
        Recursive reconstruction of the path from start to end (excluded)
        :param pile: pile
        :param start: (int, int)
        :param end: (int, int)
        """
        middle = tuple(P[start[0], start[1], end[0], end[1]])

        if middle == (-1, -1):
            debug.debug_play("Error rebuilding path: unknown precedent")
        elif start == end:
            debug.debug_play("Error rebuilding path: start = end")
        elif is_neighboring(start, end, distance=1, board=board) or is_neighboring(start, end, distance=2, board=board):
            pile.append(start)
        else:
            aux(pile, start, middle)
            aux(pile, middle, end)

    pile = []
    aux(pile, start, end)
    pile.append(end)

    return np.array(pile)


def get_move(path : [(int, int)], board : np.ndarray) -> (int, int):
    """
    Get move to play from path
    :param path: tuple list
    :param board: board
    :return: move
    """
    U = get_poisson(board)

    X, Y = path.T
    i = np.argmax(U[X, Y])

    return X[i], Y[i]
