import numpy


def init_board(size: int = 11, board: numpy.ndarray = None) -> numpy.ndarray:
    """
    Create new Hex Game
    :param board: Board to load
    :param size: Size of the game to create
    :return board
    """
    if board is None:
        board = -numpy.ones((size + 2, size + 2))
    board[0, :] = 0
    board[-1, :] = 0
    board[:, -1] = 1
    board[:, 0] = 1
    return board


def play_move(board: numpy.ndarray, x: int, y: int, player: int) -> numpy.ndarray:
    """
    Make player play a move
    :param board: board
    :param x: x position of the move
    :param y: y position of the move
    :param player: player playing
    :return: Whether or not the move succeed
    """
    if 0 < x < board.shape[0] - 1 > y > 0 and board[x, y] == -1:
        board[x, y] = player
        return True
    else:
        return False


def has_win(board: numpy.ndarray, player: int) -> bool:
    """
    Check if a player has win
    :param board: board
    :param player: int corresponding to the player (0 or 1)
    :return: Whether or not player has win
    """
    checked = numpy.zeros(board.shape, dtype=bool)
    pile = []
    size = board.shape[0]

    # Append edges
    for a in range(1, size - 1):
        if player == 0 and board[1, a] == 0:
            pile.append((1, a))
        elif player == 1 and board[a, 1] == 1:
            pile.append((a, 1))

    # Process tiles
    while len(pile) != 0:
        x, y = pile.pop()

        if 0 < x < size - 1 > y > 0 and board[x, y] == player and not checked[x, y]:

            if (x == size - 2 and player == 0) or (y == size - 2 and player == 1):
                return True

            checked[x, y] = True
            pile.append((x - 1, y))
            pile.append((x + 1, y))
            pile.append((x, y - 1))
            pile.append((x, y + 1))
            pile.append((x + 1, y - 1))
            pile.append((x - 1, y + 1))

    return False
