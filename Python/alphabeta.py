import numpy
import hex_game
from tools import *
from player import Player


class PlayerAlphaBeta(Player):
    def init(self, renderer):
        pass

    def play_move(self, player: int, board: numpy.ndarray) -> PlayerResponse:
        self.count = 0
        depth = 4
        moves = get_possibles_moves(board)
        scores = [-self.alphabeta(play_move_and_copy(board, moves[i], player), depth - 1, 1 - player, -float('inf'),
                                  float('inf'))
                  for i in range(len(moves))]
        move = moves[numpy.argmax(scores)]

        success = can_play_move(board, move)

        message = "Computation done in {} iterations".format(self.count)

        return {'move': move, 'success': success, 'message': message}

    def alphabeta(self, board: numpy.ndarray, depth: int, player: int, alpha: float, beta: float):
        if depth == 0:
            return get_scores(board)[0][player]
        else:
            moves = get_possibles_moves(board)
            if len(moves) == 0:
                return get_scores(board)[0][player]
            else:
                u = -float('inf')
                for move in moves:
                    val = -self.alphabeta(play_move_and_copy(board, move, player), depth - 1, 1 - player, - alpha,
                                          -beta)
                    if val > u:
                        u = val
                        if u > alpha:
                            alpha = u
                            if alpha >= beta:
                                return u
                return u
