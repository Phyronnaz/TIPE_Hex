import random

import numpy

from hex_game.player_human import HumanPlayer


class PathAI:
    NEIGHBORS_1 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
    NEIGHBORS_2 = [(-1, 2), (1, 1), (2, -1), (1, -2), (-1, -1), (-2, 1)]

    def __init__(self):
        self.human = HumanPlayer()

    def init(self, renderer):
        self.renderer = renderer
        self.human.init(renderer)

    def play_move(self, player, hex_game):
        """
        Play a move
        :param player: Player playing
        :param hex_game: Hex Game to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        self.renderer.clear_lines()
        groups = [self.get_groups(hex_game.board, 0), self.get_groups(hex_game.board, 1)]

        if len(groups[0]) > 0 and len(groups[1]) > 0:
            scores = [[], []]

            for k in [0, 1]:
                for g in groups[k]:
                    l = []
                    for c in g:
                        l.append(c[0])
                        l.append(c[1])
                    maximum = max(l, key=lambda t: t[k])[k]
                    minimum = min(l, key=lambda t: t[k])[k]

                    scores[k].append(maximum - minimum)

            bests = [groups[0][numpy.argmax(scores[0])], groups[1][numpy.argmax(scores[1])]]
            score = [scores[0][numpy.argmax(scores[0])] for k in [0, 1]]
            # print(score[0])
            # print(score[1])
            # print("///////////////////////////")
            if score[player] < score[1 - player]:
                move = PathAI.counter(bests[1 - player], hex_game.board, player)
            else:
                move = PathAI.counter_counter(bests[player], hex_game.board, player)
                if move is None:
                    move = PathAI.continue_path(bests[player], hex_game.board, player)
        else:
            move = PathAI.start(hex_game.board, player)

        return hex_game.play_move(move[0] - 1, move[1] - 1, player)

    def get_groups(self, board, player):
        """
        Detect groups of tile on board for player
        :param board: game board
        :param player: player to check
        :return: array of array of (p1, p2, x) tuples where p1, p2 are positions and x the space between p1 and p2
        """
        # Generate couples
        couples = []
        size = board.shape[0]
        for i in range(size):
            for j in range(size):
                if board[i, j] == player:
                    l0 = [(i + x, j + y) for x, y in self.NEIGHBORS_1]
                    l1 = [(i + x, j + y) for x, y in self.NEIGHBORS_2]
                    for p in l0 + l1:
                        border = (i == 0 and p[0] == 0) or (i == size - 1 and p[0] == size - 1) or \
                                 (j == 0 and p[1] == 0) or (j == size - 1 and p[1] == size - 1)
                        if 0 <= p[0] < size and 0 <= p[1] < size and board[p] == player and not border:
                            # self.renderer.create_hexagon(p2[0], p2[1], "pink", transparent=True)
                            if p in l0:
                                couples.append(((i, j), p, 0))
                            else:
                                # for a, b in self.get_common_neighbours([i, j], p):
                                #    self.renderer.create_hexagon(a, b, "green", transparent=True)
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

        b = True
        while b:
            b = fusion(groups)

        # Debug groups
        for g in groups:
            color = "#" + ("%06x" % random.randint(0, 16777215))
            for c in g:
                self.renderer.create_line(c[0] - numpy.ones(2), c[1] - numpy.ones(2), color)

        return numpy.array(groups)

    @staticmethod
    def start(board, player):
        print("Start")
        for p in [(6, 6), (7, 4), (8, 3)]:
            if board[p] == -1:
                return p

    @staticmethod
    def counter(group, board, player):
        print("Counter")
        move = (0, 0)
        return move

    @staticmethod
    def counter_counter(group, board, player):
        for c in group:
            if c[2] == 1:
                p1, p2 = PathAI.get_common_neighbours(c[0], c[1])
                if board[p1] == -1 and board[p2] == 1 - player:
                    print("Counter counter")
                    return p1
                elif board[p2] == -1 and board[p1] == 1 - player:
                    print("Counter counter")
                    return p2

        return None

    @staticmethod
    def continue_path(group, board, player):
        print("Continue path")
        size = board.shape[0] - 1
        tiles = []

        for c in group:
            tiles.append(c[0])
            tiles.append(c[1])

        maximum = max(tiles, key=lambda t: t[player])
        minimum = min(tiles, key=lambda t: t[player])

        print(minimum)
        print(maximum)

        if maximum[player] - minimum[player] == size:
            print("Complete path")
            move = PathAI.complete_path(group, board)
        elif maximum[player] > size - minimum[player] and minimum[player] != 0:
            side = [0, 0]
            side[player] = -1
            move = PathAI.get_next(side, board, minimum)
        elif maximum[player] != board.shape[0] - 1:
            side = [0, 0]
            side[player] = 1
            move = PathAI.get_next(side, board, maximum)
        else:
            print("No move")

        return move

    @staticmethod
    def complete_path(group, board):
        for c in group:
            if c[2] == 1:
                p1, p2 = PathAI.get_common_neighbours(c[0], c[1])
                if board[p1] == -1 and board[p2] == -1:
                    return p1

    @staticmethod
    def get_next(side, board, p):
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

        def check(a):
            return 1 <= a[0] < board.shape[0] - 1 > a[1] >= 1 and board[a[0], a[1]] == -1

        p1 = numpy.array(PathAI.NEIGHBORS_2[i]) + p
        p2 = numpy.array(PathAI.NEIGHBORS_2[i - 1]) + p
        p3 = numpy.array(PathAI.NEIGHBORS_2[(i + 1) % 6]) + p
        possibilities = [p1]
        possibilities += PathAI.get_common_neighbours(p1, p)
        possibilities += PathAI.get_common_neighbours(p2, p)
        possibilities += PathAI.get_common_neighbours(p3, p)
        possibilities += [p2]
        possibilities += [p3]

        for x in possibilities:
            if check(x):
                return x

        print("Error: No next to play")

    @staticmethod
    def get_common_neighbours(p1, p2):
        """
        Get common neighbours of points p1 and p2
        :param p1: point 1
        :param p2: point 2
        :return: list of tuple
        """
        i, j = p1
        l1 = [(i + x, j + y) for x, y in PathAI.NEIGHBORS_1]
        i, j = p2
        l2 = [(i + x, j + y) for x, y in PathAI.NEIGHBORS_1]
        return [k for k in l1 if k in l2]
