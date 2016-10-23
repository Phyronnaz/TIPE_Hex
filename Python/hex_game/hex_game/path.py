import numpy

import hex_game.tools as tools
from hex_game.tools import Position


def join(board: numpy.ndarray, point: Position, player: int) -> Position:
    middle = board.shape[player] // 2
    side = [0, 0]
    side[player] = int(middle > point[player])
    move = tools.get_next(tuple(side), point, True)
    return move
