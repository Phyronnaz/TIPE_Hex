import random

import numpy

from hex_game.player_human import HumanPlayer


class PathAI:
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
            print(score[0])
            print(score[1])
            print("///////////////////////////")
            if score[player] < score[1 - player]:
                move = self.counter(bests[1 - player], hex_game.board, player)
            else:
                move = self.continue_path(bests[player], hex_game.board, player)
        else:
            if hex_game.get_tile(5, 5) == 0:
                move = (5, 5)
            else:
                move = (6, 3)

        return hex_game.play_move(move[0], move[1], player)

    def get_groups(self, board, player):
        """
        Detect groups of tile on board for player
        :param board: game board
        :param player: player to check
        :return: array of array of (p1, p2, x) tuples where p1, p2 are positions and x the space between p1 and p2
        """
        # Generate couples
        couples = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] == player:
                    l0 = [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1], [i - 1, j + 1], [i + 1, j - 1]]
                    l1 = [[i - 1, j - 1], [i - 2, j + 1], [i - 1, j + 2], [i + 1, j + 1], [i + 2, j - 1],
                          [i + 1, j - 2]]
                    for p in l0 + l1:
                        if 0 <= p[0] < board.shape[0] and 0 <= p[1] < board.shape[1] and board[p[0], p[1]] == player:
                            # self.renderer.create_hexagon(p2[0], p2[1], "pink", transparent=True)
                            if p in l0:
                                couples.append(([i, j], p, 0))
                            else:
                                # for a, b in self.get_common_neighbours([i, j], p):
                                #    self.renderer.create_hexagon(a, b, "green", transparent=True)
                                couples.append(([i, j], p, 1))

        # Group couples
        groups = [[k] for k in couples]

        def fusion(groups):
            for group1 in groups:
                for group2 in groups:
                    if group1 != group2:
                        for c1 in group1:
                            for c2 in group2:
                                if c1[0] == c2[0] or c1[0] == c2[1] or c1[1] == c2[0] or c1[1] == c2[1]:
                                    group1.extend(group2)
                                    groups.remove(group2)
                                    return True
            return False

        b = True
        while b:
            b = fusion(groups)

        # Debug groups
        for g in groups:
            color = "#" + ("%06x" % random.randint(0, 16777215))
            for c in g:
                self.renderer.create_line(c[0], c[1], color)
        return numpy.array(groups)

    def counter(self, group, board, player):
        move = (0, 0)
        return move

    def continue_path(self, group, board, player):
        l = []
        for c in group:
            l.append(c[0])
            l.append(c[1])
        maximum = max(l, key=lambda t: t[player])
        minimum = min(l, key=lambda t: t[player])
        if minimum[player] > 10 - maximum[player]:
            side = [0, 0]
            side[player] = -1
            move = self.get_next(side, board, minimum)
        else:
            side = [0, 0]
            side[player] = 1
            move = self.get_next(side, board, maximum)
        return move

    @staticmethod
    def get_next(side, board, p):
        p = numpy.array(p)
        if side == [1, 0]:
            x = p + numpy.array([2, -1])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([1, -2])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([1, 1])
            if board[x[0], x[1]] == 0:
                return x

        if side == [-1, 0]:
            x = p + numpy.array([-2, 1])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([-1, 2])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([-1, -1])
            if board[x[0], x[1]] == 0:
                return x

        if side == [0, 1]:
            x = p + numpy.array([-1, 2])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([-2, 1])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([1, 1])
            if board[x[0], x[1]] == 0:
                return x

        if side == [0, -1]:
            x = p + numpy.array([1, -2])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([-1, -1])
            if board[x[0], x[1]] == 0:
                return x
            x = p + numpy.array([2, -1])
            if board[x[0], x[1]] == 0:
                return x

    def get_common_neighbours(p1, p2):
        """
        Get common neighbours of points p1 and p2
        :param p1: point 1
        :param p2: point 2
        :return: list of tuple
        """
        x, y = p1
        l1 = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
        x, y = p2
        l2 = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
        return [k for k in l1 if k in l2]
