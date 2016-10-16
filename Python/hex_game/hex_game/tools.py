import numpy

NEIGHBORS_1 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
NEIGHBORS_2 = [(-1, 2), (1, 1), (2, -1), (1, -2), (-1, -1), (-2, 1)]


def get_groups(board, player):
    """
    Detect groups of tile on board for player
    :param board: game board
    :param player: player to check
    :return: array of array of (p1, p2, x) tuples where p1, p2 are positions and x the space between p1 and p2
    """
    # Generate couples
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
                            if player not in [board[p1], board[p2]] and (board[p1] == -1 or board[p2] == -1):
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

    return numpy.array(groups)


def get_scores(board, groups=None, best=False):
    """
    Get score of a board
    :param board: numpy array
    :param groups: precomputed groups
    :param best : return best groups index
    :return: [score_player_0, score_player_1] [, best]
    """
    if groups is None:
        groups = [get_groups(board, k) for k in [0, 1]]

    scores = [[], []]

    for k in [0, 1]:
        for g in groups[k]:
            l = []
            for c in g:
                l.append(c[0])
                if c[2] != -1:
                    l.append(c[1])

            maximum = max(l, key=lambda t: t[k])[k]
            minimum = min(l, key=lambda t: t[k])[k]

            scores[k].append(maximum - minimum)

    best_scores = [scores[k][numpy.argmax(scores[k])] if len(scores[k]) > 0 else 0 for k in [0, 1]]
    bests = [numpy.argmax(scores[k]) if len(scores[k]) > 0 else -1 for k in [0, 1]]
    if best:
        return best_scores, bests
    else:
        return best_scores


def get_next(side, board, p, far):  # TODO: not checked
    side = numpy.array(side).tolist()
    p = numpy.array(p)

    if side == [0, 1]:
        i = 0
    elif side == [1, 1]:
        i = 1
    elif side == [1, -1]:
        i = 2
    elif side == [0, -1]:
        i = 3
    elif side == [-1, -1]:
        i = 4
    elif side == [-1, 1]:
        i = 5
    elif side == [-1, 0]:
        i = 5
    elif side == [1, 0]:
        i = 2

    def check(a):
        return 1 <= a[0] < board.shape[0] - 1 > a[1] >= 1 and board[a[0], a[1]] == -1

    possibilities = []

    if far:
        p1 = numpy.array(NEIGHBORS_2[i]) + p
        p2 = numpy.array(NEIGHBORS_2[i - 1]) + p
        p3 = numpy.array(NEIGHBORS_2[(i + 1) % 6]) + p
        possibilities += [p1]
        possibilities += get_common_neighbours(p1, p)
        possibilities += get_common_neighbours(p2, p)
        possibilities += get_common_neighbours(p3, p)
        possibilities += [p2]
        possibilities += [p3]
    else:
        possibilities += [numpy.array(NEIGHBORS_1[i]) + p]
        possibilities += [numpy.array(NEIGHBORS_1[i - 1]) + p]
        possibilities += [numpy.array(NEIGHBORS_1[(i + 1) % 6]) + p]

    for x in possibilities:
        if check(x):
            return x

    print("Error: No next tile for " + str(p))
    return None


def get_common_neighbours(p1, p2):
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
