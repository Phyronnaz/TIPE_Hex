import numpy
import hex_game
from tools import *


class PlayerAlphaBeta:
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
            [-self.alphabeta(hex_game.play_move_and_copy(board, move[0], move[1], player), depth, 1 - player, -float.infinity, float.infinity) for move in
             moves])]
        return hex_game.play_move(board, move[0], move[1], player)



    def alphabeta(self, board: numpy.ndarray, depth: int, player: int, alpha: float, beta: float):

        if depth == 0:
            return hex_game.get_scores(board)[0][player]
        else:
            moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
            if len(moves) == 0:
                return hex_game.get_scores(board)[0][player]
            else:
                u = -float.infinity
                for move in moves:
                    val = -alphabeta(self, hex_game.play_move_and_copy(board, move[0], move[1], player), depth - 1, 1 - player - alpha, -beta)
                    if val > u:
                        u = val
                        if u > alpha:
                            alpha = u
                            if alpha >= beta:
                                return (u)
                return (u)
