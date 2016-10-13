import random

import numpy

import hex_game.tools as tools
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
        :return: 0 : fail, 1 : success, 2 : wait
        """
        self.renderer.clear_lines()
        print("///////////////////////////")

        groups = [tools.get_groups(hex_game.board, k) for k in [0, 1]]
        scores, best_indices = tools.get_scores(hex_game.board, groups=groups, best=True)

        if -1 not in best_indices:
            best_groups = [groups[k][best_indices[k]] for k in [0, 1]]

            # Debug groups and scores

            # for c in best_groups[player]:
            #     if c[2] == 1:
            #         p = tools.get_common_neighbours(c[0], c[1])[0]
            #         self.renderer.create_hexagon(p[0] - 1, p[1] - 1, "pink", transparent=True)
            for k in [0, 1]:
                for g in groups[k]:
                    color = "#" + ("%06x" % random.randint(0, 16777215))
                    for c in g:
                        self.renderer.create_line(c[0] - numpy.ones(2), c[1] - numpy.ones(2), color)

            print("Player 0 score : " + str(scores[0]))
            print("Player 1 score : " + str(scores[1]))

            choice = PathAI.choose_state(hex_game.board, player, scores, best_groups)
            if choice == 0:
                move = PathAI.first_move(hex_game.board, player)
            elif choice == 1:
                move = PathAI.counter(hex_game.board, player, best_groups[1 - player])
            elif choice == 2:
                move = PathAI.counter_counter(hex_game.board, player, best_groups[player])
            elif choice == 3:
                move = PathAI.continue_path(hex_game.board, player, best_groups[player])
            elif choice == 4:
                move = PathAI.complete_path(hex_game.board, best_groups[player])
        else:
            move = PathAI.first_move(hex_game.board, player)

        print("///////////////////////////")
        return hex_game.play_move(move[0] - 1, move[1] - 1, player)

    @staticmethod
    def choose_state(board, player, scores, best_groups):
        """
        Return the state to play
        :param board: board
        :param player: player
        :return: 0 : start, 1 : counter, 2 : counter counter, 3 : continue_path, 4 : complete_path
        """
        choice = 0
        if scores[player] < scores[1 - player]:  # Counter
            choice = 1
        elif PathAI.counter_counter(board, player, best_groups[player]) is not None:  # Try counter counter
            choice = 2
        elif scores[player] == board.shape[0] - 1:  # Complete path
            choice = 4
        else:  # Continue path
            choice = 3

        return choice

    @staticmethod
    def first_move(board, player):
        print("First move")
        return 3, 5

    @staticmethod
    def counter(board, player, group):
        print("Counter")
        move = (0, 0)
        return move

    @staticmethod
    def counter_counter(board, player, group):
        for c in group:
            if c[2] == 1:
                print(c)
                p1, p2 = tools.get_common_neighbours(c[0], c[1])
                if board[p1] == -1 and board[p2] == 1 - player:
                    print("Counter counter")
                    return p1
                elif board[p2] == -1 and board[p1] == 1 - player:
                    print("Counter counter")
                    return p2

        return None

    @staticmethod
    def continue_path(board, player, group):
        print("Continue path")
        move = None
        size = board.shape[0] - 1

        tiles = []
        for c in group:
            tiles.append(c[0])
            if c[2] != -1:
                tiles.append(c[1])
        if len(tiles) == 0:
            return move

        maximum = max(tiles, key=lambda t: t[player])  # TODO : put in tools
        minimum = min(tiles, key=lambda t: t[player])

        if maximum[player] > size - minimum[player] and minimum[player] != 0:
            side = [0, 0]
            side[player] = -1
            move = tools.get_next(side, board, minimum)
        elif maximum[player] != board.shape[0] - 1:
            side = [0, 0]
            side[player] = 1
            move = tools.get_next(side, board, maximum)
        else:
            print("No move")

        return move

    @staticmethod
    def complete_path(board, group):
        print("Complete path")
        for c in group:
            if c[2] == 1:
                p1, p2 = tools.get_common_neighbours(c[0], c[1])
                if board[p1] == -1 and board[p2] == -1:
                    return p1
        print("No path completion found")
