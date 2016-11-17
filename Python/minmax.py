import numpy
from hex_game import *
from tools import *


class PlayerMiniMax:
    def init(self, renderer):
        pass

    def play_move(self, player: int, board: numpy.ndarray) -> bool:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        self.count = 0
        depth = 9000
        moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
        move = moves[numpy.argmax(
            [-self.minimax(play_move_copy(board, move[0], move[1], player), depth, 1 - player) for move in
             moves])]
        return play_move(board, move[0], move[1], player)

    def minimax(self, board: numpy.ndarray, depth: int, player: int) -> float:
        """

        :param board: numpy array
        :param depth: int
        :param play_move: param : board, player, move -> board
        :param get_score: param : board, -> score player0 - score player1
        :param get_moves: param : board, player -> tuple list
        :return: score player0-score player1
        """
        self.count += 1
        if self.count % 100 == 0:
            print(self.count)
        if depth == 0:
            return get_scores(board)[0][player]
        else:
            if has_win(board, player) or has_win(board, 1 - player):
                return get_scores(board)[0][player]
            else:
                moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
                return max(
                    [-self.minimax(play_move_copy(board, move[0], move[1], player), depth - 1, 1 - player)
                     for move in moves])

    def alphabeta(self, board: numpy.ndarray, depth: int, player: int, alpha: float, beta: float):

        if depth == 0:
            return get_scores(board)[0][player]
        else:
            moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
            if len(moves) == 0:
                return get_scores(board)[0][player]
            else:
                u = -float('inf')
                for move in moves:
                    val = -self.alphabeta(self, play_move_copy(board, move[0], move[1], player), depth - 1,
                                     1 - player - alpha, -beta)
                    if val > u:
                        u = val
                        if u > alpha:
                            alpha = u
                            if alpha >= beta:
                                return u
                return u
