import numpy

NEIGHBORS_1 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
NEIGHBORS_2 = [(-1, 2), (1, 1), (2, -1), (1, -2), (-1, -1), (-2, 1)]


#  -------------> y
# |  000000000
# | 1
# | 1
# | 1
# | 1
# v
# x

def init_board(size: int = 11) -> numpy.ndarray:
    """
    Create new Hex Game
    :param size: Size of the game to create
    :return board
    """
    return -numpy.ones((size, size), dtype=int)


def play_move(board: numpy.ndarray, move: (int, int), player: int) -> None:
    """
    Make player play move
    :param board: board
    :param move: move
    :param player: player playing
    """
    board[move] = player


def can_play_move(board: numpy.ndarray, move: (int, int)) -> bool:
    """
    Check if player can play move
    :param board: board
    :param move: move
    :return: Whether or not he can succeed
    """
    return 0 <= move[0] < board.shape[0] > move[1] >= 0 and board[move[0], move[1]] == -1


def play_move_and_copy(board: numpy.ndarray, move: (int, int), player: int) -> numpy.ndarray:
    """
    Make player play a move and return new board
    :param board: board
    :param move: move
    :param player: player playing
    :return: Whether or not the move succeed
    """
    new_board = board.copy()
    new_board[move] = player
    return new_board


def has_win(board: numpy.ndarray, player: int) -> bool:
    """
    Check if a player has win
    :param board: board
    :param player: int corresponding to the player (0 or 1)
    :return: Whether or not player has win
    """
    checked = numpy.zeros(board.shape, dtype=bool)
    size = board.shape[0]
    pile = []

    # Append edges
    for a in range(size):
        if player == 0 and board[0, a] == 0:
            pile.append((0, a))
        elif player == 1 and board[a, 0] == 1:
            pile.append((a, 0))

    # Process tiles
    while len(pile) != 0:
        x, y = pile.pop()

        if 0 <= x < size and 0 <= y < size and board[x, y] == player and not checked[x, y]:

            if (x == size - 1 and player == 0) or (y == size - 1 and player == 1):
                return True

            checked[x, y] = True
            pile.append((x - 1, y))
            pile.append((x + 1, y))
            pile.append((x, y - 1))
            pile.append((x, y + 1))
            pile.append((x + 1, y - 1))
            pile.append((x - 1, y + 1))

    return False


def get_possibles_moves(board: numpy.ndarray) -> [(int, int)]:
    """
    Get all possibles moves
    """
    return [tuple(k) for k in numpy.argwhere(board == -1)]


def get_random_move(board: numpy.ndarray) -> (int, int):
    """
    Random move
    :param board: board
    :return: (int, int)
    """
    moves = get_possibles_moves(board)
    numpy.random.shuffle(moves)

    return moves[0]


def is_neighboring(a: (int, int), b: (int, int), distance: int, board: numpy.ndarray) -> bool:
    """
    Are a and b neighbors?
    :param a: (int, int)
    :param b: (int, int)
    :param distance: 1 or 2
    :return: bool
    """
    if distance == 1:
        return a in get_neighbors_1(b, board)
    else:
        return a in get_neighbors_2(b, board)


def get_common_neighbors(p1: (int, int), p2: (int, int), board: numpy.ndarray) -> [(int, int)]:
    """
    Get common neighbours of points p1 and p2
    :param p1: point 1
    :param p2: point 2
    :param board: board
    :return: list of tuple
    """
    l1 = get_neighbors_1(p1, board)
    l2 = get_neighbors_1(p2, board)
    return [k for k in l1 if k in l2]


def get_neighbors_1(p: (int, int), board: numpy.ndarray) -> [(int, int)]:
    """
    Return a list of all NEIGHBORS_1 of p in board
    :param p: (x, y)
    :param board: board
    :return: list[(int, int)]
    """
    n = board.shape[0]
    a, b = p
    return [(a + i, b + j) for (i, j) in NEIGHBORS_1 if 0 <= a + i < n > b + j >= 0]


def get_neighbors_2(p: (int, int), board: numpy.ndarray) -> list((int, int)):
    """
    Return a list of all NEIGHBORS_2 of p in board
    :param p: (x, y)
    :param board: board
    :return: list[(int, int)]
    """
    a, b = p
    n = board.shape[0]
    return [(a + i, b + j) for (i, j) in NEIGHBORS_2
            if 0 <= a + i < n > b + j >= 0 and
            len([k for k in get_common_neighbors(p, (a + i, b + j), board) if board[k] == -1]) == 2]


def add_edges(board: numpy.ndarray, count: int) -> numpy.ndarray:
    n = board.shape[0]
    B = -numpy.ones((n + 2 * count, n + 2 * count), dtype=int)  # Large board
    B[count:n + count, count:n + count] = board

    # Set edges values
    B[:count, :] = 0
    B[-count:, :] = 0

    B[:, :count] = 1
    B[:, -count:] = 1

    B[:count, :count] = -1
    B[-count:, -count:] = -1

    B[:count, -count:] = -1
    B[-count:, :count] = -1

    return B


def invert_path(path: [(int, int)], player: int) -> [(int, int)]:
    """
    Invert moves of path path
    :param path: path
    :param player: 0 or 1
    :return: list((int, int))
    """
    return [invert_move(k, player) for k in path]


def invert_board(board: numpy.ndarray, player: int) -> numpy.ndarray:
    """
    Invert board board
    :param board: board
    :param player: 0 or 1
    :return: copy of inverted board
    """
    board = board.copy()

    if player == 1:
        board = board.T
        p0 = board == 0
        p1 = board == 1
        board[p0] = 1
        board[p1] = 0

    return board


def invert_move(move: (int, int), player: int) -> (int, int):
    """
    Invert a move
    :param move: (int, int)
    :param player: 0 or 1
    :return: (int, int)
    """
    if player == 0:
        return move[0], move[1]
    else:
        return move[1], move[0]

def flip(board: numpy.ndarray) -> numpy.ndarray:
    """
    Flip a board
    :param board: board 
    :return: flipped board
    """
    return board[::-1, ::-1]