import numpy
from typing import Tuple, List, Union, Dict

# Move in real position (visual position + (1, 1))
Move = Tuple[int, int]
Position = Tuple[int, int]
Couple = Tuple[Position, Position, int]
Group = List[Couple]
Path = List[Position]
# Zip {move: Move, success: bool, message: str (optional) , player_class: str (optional)}
PlayerResponse = Dict[str, Union[Move, bool, str]]

NEIGHBORS_1 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
NEIGHBORS_2 = [(-1, 2), (1, 1), (2, -1), (1, -2), (-1, -1), (-2, 1)]


def init_board(visual_size: int = 11, board: numpy.ndarray = None) -> numpy.ndarray:
    """
    Create new Hex Game
    :param board: Board to load
    :param visual_size: Size of the game to create
    :return board
    """
    if board is None:
        board = -numpy.ones((visual_size + 2, visual_size + 2), dtype=int)
    board[0, :] = 0
    board[-1, :] = 0
    board[:, -1] = 1
    board[:, 0] = 1
    return board


def play_move(board: numpy.ndarray, move: Move, player: int) -> None:
    """
    Make player play move
    :param board: board
    :param move: move
    :param player: player playing
    :return: Whether or not the move succeed
    """
    board[move] = player


def can_play_move(board: numpy.ndarray, move: Move) -> bool:
    """
    Check if player can play move
    :param board: board
    :param move: move
    :return: Whether or not he can succeed
    """
    if 0 < move[0] < board.shape[0] - 1 > move[1] > 0 and board[move] == -1:
        return True
    else:
        return False


def play_move_and_copy(board: numpy.ndarray, move: Move, player: int) -> numpy.ndarray:
    """
    Make player play a move and return new board
    :param board: board
    :param move: move
    :param player: player playing
    :return: Whether or not the move succeed
    """
    if 0 < move[0] < board.shape[0] - 1 > move[1] > 0 and board[move] == -1:
        new_board = board.copy()
        new_board[move] = player
        return new_board
    else:
        return None


def has_win(board: numpy.ndarray, player: int) -> bool:
    """
    Check if a player has win
    :param board: board
    :param player: int corresponding to the player (0 or 1)
    :return: Whether or not player has win
    """
    checked = numpy.zeros(board.shape, dtype=bool)
    pile = []

    # Append edges
    for a in range(1, board.shape[0] - 1):
        if player == 1 and board[a, 0] == 1:
            pile.append((a, 0))
    for a in range(1, board.shape[1] - 1):
        if player == 0 and board[0, a] == 0:
            pile.append((0, a))

    # Process tiles
    while len(pile) != 0:
        x, y = pile.pop()

        in_bounds = 0 <= x < board.shape[0] and 0 <= y < board.shape[1]
        if in_bounds and board[x, y] == player and not checked[x, y]:
            if (x == board.shape[0] - 1 and player == 0) or (y == board.shape[1] - 1 and player == 1):
                return True

            checked[x, y] = True
            pile.append((x - 1, y))
            pile.append((x + 1, y))
            pile.append((x, y - 1))
            pile.append((x, y + 1))
            pile.append((x + 1, y - 1))
            pile.append((x - 1, y + 1))

    return False
