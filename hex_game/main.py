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
    return 0 <= move[0] < board.shape[0] > move[1] >= 0 and board[move] == -1


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


def has_win(board: numpy.ndarray, player: int):
    """
    Check if a player has win
    :param board: board
    :param player: int corresponding to the player (1 or 2)
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


def get_possibles_moves(board: numpy.ndarray) -> list((int, int)):
    """
    Get all possibles moves
    """
    return [tuple(k) for k in numpy.argwhere(board == -1)]


def get_random_move(board: numpy.ndarray, state: numpy.random.RandomState):
    moves = get_possibles_moves(board)
    state.shuffle(moves)

    return moves[0]


def is_neighboring(a, b):
    for (k, l) in NEIGHBORS_1:
        if a[0] == b[0] + k and a[1] == b[1] + l:
            return True
    return False
