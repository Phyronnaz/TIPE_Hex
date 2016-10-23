from typing import Tuple, List

import numpy

import hex_game.hex_game as hex
import hex_game.tools as tools
from hex_game.player_human import HumanPlayer
from hex_game.renderer import Renderer
from hex_game.tools import Group, Position

Move = List[Tuple[int, Position]]


class PathAI:
    def __init__(self):
        self.human = HumanPlayer()
        self.renderer = None

    def init(self, renderer: Renderer):
        self.renderer = renderer
        self.human.init(renderer)

    def play_move(self, player: int, board: numpy.ndarray) -> bool:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: 0 : fail, 1 : success, 2 : wait
        """
        groups = tuple([tools.get_groups(board, k) for k in [0, 1]])
        scores, best_indices = tools.get_scores(board, groups=groups)

        if -1 not in best_indices:
            best_groups = tuple([groups[k][best_indices[k]] for k in [0, 1]])

            print("Player 0 score : " + str(scores[0]))
            print("Player 1 score : " + str(scores[1]))

            choice = PathAI.choose_state(board, player, scores, best_groups)
            if choice == 0:
                moves = PathAI.first_move(board, player)
            elif choice == 1:
                moves = PathAI.counter(board, player, best_groups[1 - player])
            elif choice == 2:
                moves = PathAI.counter_counter(board, player, best_groups[player])
            elif choice == 3:
                moves = PathAI.continue_path(board, player, best_groups[player])
            elif choice == 4:
                moves = PathAI.complete_path(board, best_groups[player])
        else:
            moves = PathAI.first_move(board, player)
        move = min(moves)[1]
        return hex.play_move(board, move[0], move[1], player)

    @staticmethod
    def choose_state(board: numpy.ndarray, player: int, scores: Tuple[int, int],
                     best_groups: Tuple[List[Group], List[Group]]) -> int:
        """
        Return the state to play
        :param board: board
        :param player: player
        :param scores: scores of the players
        :param best_groups: best group for each player
        :return: 0 : start, 1 : counter, 2 : counter counter, 3 : continue_path, 4 : complete_path
        """
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
    def first_move(board: numpy.ndarray, player: int) -> List[Move]:
        print("First move")
        size = board.shape[0] - 1
        s = (size // 2, size // 2)
        moves = [(0, s)]
        for p in tools.NEIGHBORS_1:
            moves.append((len(moves), (s[0] + p[0], s[1] + p[1])))
        return moves

    @staticmethod
    def counter(board: numpy.ndarray, player: int, group: Group) -> List[Move]:
        """
        Counter a group
        :param board: board
        :param player: player who counter
        :param group: group to counter
        :return: moves to play
        """
        print("Counter")
        size = board.shape[0]
        minimum, maximum = tools.get_bounds(group, 1 - player)

        side = [0, 0]
        best, side[1 - player] = (maximum, 1) if minimum[1 - player] > size - maximum[1 - player] else (minimum, -1)

        next_0 = tools.get_next(tuple(side), best, True)
        next_1 = tools.get_next(tuple(side), next_0, False)
        if board[next_1] == -1:
            move = next_1
        elif board[next_1] == player:
            side = [0, 0]
            side[player] = 1
            next_2 = tools.get_next(tuple(side), next_1, True)
            if board[next_2] == -1:
                move = next_2
            else:
                side = [0, 0]
                side[player] = -1
                next_3 = tools.get_next(tuple(side), next_1, False)
                move = next_3

        return [(0, move)]

    @staticmethod
    def counter_counter(board: numpy.ndarray, player: int, group: Group) -> List[Move]:
        moves = []
        for c in group:
            if c[2] == 1:
                p1, p2 = tools.get_common_neighbours(c[0], c[1])
                if board[p1] == -1 and board[p2] == 1 - player:
                    moves += [(len(moves), p1)]
                elif board[p2] == -1 and board[p1] == 1 - player:
                    moves += [(len(moves), p2)]
        if len(moves) == 0:
            return None
        else:
            print("Counter counter")
            return moves

    @staticmethod
    def continue_path(board: numpy.ndarray, player: int, group: Group) -> List[Move]:
        print("Continue path")
        size = board.shape[0] - 1
        minimum, maximum = tools.get_bounds(group, player)

        move_minimum = None
        move_maximum = None
        if minimum[player] != 0:
            side = [0, 0]
            side[player] = -1
            move_minimum = tools.get_next(tuple(side), minimum, True)
        if maximum[player] != size:
            side = [0, 0]
            side[player] = 1
            move_maximum = tools.get_next(tuple(side), maximum, True)

        moves = []
        if move_maximum is None and move_minimum is None:
            raise Exception("No move left")
        elif move_minimum is None:
            moves.append((0, move_maximum))
        elif move_maximum is None:
            moves.append((0, move_minimum))
        else:
            x = int(minimum[player] > size - maximum[player])
            moves.append((x, move_maximum))
            moves.append((1 - x, move_minimum))
        return moves

    @staticmethod
    def complete_path(board: numpy.ndarray, group: Group) -> List[Move]:
        print("Complete path")
        moves = []
        for c in group:
            if c[2] == 1:
                p1, p2 = tools.get_common_neighbours(c[0], c[1])
                if board[p1] == -1 and board[p2] == -1:
                    moves += [(len(moves), p1)]
        if len(moves) == 0:
            raise Exception("No path completion found")
        else:
            return moves
