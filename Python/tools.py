import numpy
from hex_game import *

NEIGHBORS_1 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
NEIGHBORS_2 = [(-1, 2), (1, 1), (2, -1), (1, -2), (-1, -1), (-2, 1)]


def get_groups(board: numpy.ndarray, player: int) -> List[Group]:
    """
    Detect groups of tile on board for player
    :param board: game board
    :param player: player to check
    :return: array of array of (p1, p2, x) tuples where p1, p2 are positions and x the space between p1 and p2
    """
    # Generate couples
    # Array of (p1, p2, x) where x = -1 if p1 == p2, 0 if p1 and p2 are close and 1 if they are close
    couples = []
    size = board.shape[0]
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if board[i, j] == player:
                l0 = [(i + x, j + y) for x, y in NEIGHBORS_1]
                l1 = [(i + x, j + y) for x, y in NEIGHBORS_2]
                for p in l0 + l1 + [(i, j)]:
                    corner = all([x in [0, size - 1] for x in p])
                    if 0 <= p[0] < size and 0 <= p[1] < size and board[p] == player and not corner:
                        if p == (i, j):
                            couples.append(((i, j), p, -1))
                        elif p in l0:
                            couples.append(((i, j), p, 0))
                        else:
                            p1, p2 = get_common_neighbours((i, j), p)
                            if player not in [board[p1], board[p2]] and (board[p1] == -1 and board[p2] == -1):
                                couples.append(((i, j), p, 1))

    # Group couples
    groups = [[k] for k in couples]

    def fusion(f_groups):
        for group1 in f_groups:
            for group2 in f_groups:
                if group1 != group2:
                    for c1 in group1:
                        for c2 in group2:
                            if c1[0] == c2[0] or c1[0] == c2[1] or c1[1] == c2[0] or c1[1] == c2[1]:
                                group1.extend(group2)
                                f_groups.remove(group2)
                                return True
        return False

    while fusion(groups):
        pass

    return groups


def get_scores(board: numpy.ndarray, groups: Tuple[List[Group], List[Group]] = None) -> Tuple[Tuple[int, int],
                                                                                              Tuple[int, int]]:
    """
    Get score of a board
    :param board: numpy array
    :param groups: precomputed groups
    :return: (score_player_0, score_player_1), (best_player_0, bes-_player_1)
    """
    if groups is None:
        groups = [get_groups(board, k) for k in [0, 1]]

    scores = [[], []]

    for k in [0, 1]:
        for g in groups[k]:
            minimum, maximum = get_bounds(g, k)
            scores[k].append(maximum[k] - minimum[k])

    best_scores = [scores[k][numpy.argmax(scores[k])] if len(scores[k]) > 0 else 0 for k in [0, 1]]
    bests = [numpy.argmax(scores[k]) if len(scores[k]) > 0 else -1 for k in [0, 1]]
    return tuple(best_scores), tuple(bests)


def get_bounds(group: Group, player: int) -> Tuple[Position, Position]:
    """
    Get max and min tiles of a group
    :param group: group
    :param player: player
    :return: minimum, maximum
    """
    tiles = []
    for couple in group:
        tiles.append(couple[0])
        if couple[2] != -1:
            tiles.append(couple[1])

    maximum = max(tiles, key=lambda t: t[player])
    minimum = min(tiles, key=lambda t: t[player])

    return minimum, maximum


def get_next(side: Tuple[int, int], position: Position, far: bool) -> Position:
    position = numpy.array(position)
    if not far:
        if side not in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            raise Exception("Bad argument", side)
        return tuple(position + numpy.array(side))
    else:
        if side == (0, 1):
            return tuple(position + numpy.array([-1, 2]))
        elif side == (0, -1):
            return tuple(position - numpy.array([-1, 2]))
        elif side == (1, 0):
            return tuple(position + numpy.array([2, -1]))
        elif side == (-1, 0):
            return tuple(position - numpy.array([2, -1]))
        else:
            raise Exception("Bad argument", side)


def get_common_neighbours(p1: Position, p2: Position) -> List[Position]:
    """
    Get common neighbours of points p1 and p2
    :param p1: point 1
    :param p2: point 2
    :return: list of tuple
    """
    i, j = p1
    l1 = [(i + x, j + y) for x, y in NEIGHBORS_1]
    i, j = p2
    l2 = [(i + x, j + y) for x, y in NEIGHBORS_1]
    return [k for k in l1 if k in l2]


# TODO: improve
def get_move_count(board: numpy.ndarray) -> int:
    n = 0
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] in [0, 1]:
                n += 1
    return n
