import numpy
from hex_game import *
from tools import *
from ai_poisson import PoissonAI


class PlayerMiniMax:
    def play_move(self, player: int, board: numpy.ndarray) -> PlayerResponse:
        self.count = 0
        depth = 900000
        moves = get_possibles_moves(board)
        scores = [-self.negamax(play_move_and_copy(board, moves[i], player), depth - 1, 1 - player)
                  for i in range(len(moves))]
        move = moves[numpy.argmax(scores)]

        success = can_play_move(board, move)

        message = "Computation done in {} iterations".format(self.count)

        return {'move': move, 'success': success, 'message': message}

    def negamax(self, board: numpy.ndarray, depth: int, player: int) -> float:
        """

        :param board: numpy array
        :param depth: int
        :param play_move: param : board, player, move -> board
        :param get_score: param : board, -> score player0 - score player1
        :param get_moves: param : board, player -> tuple list
        :return: score player0-score player1
        """
        self.count += 1
        if self.count % 1000 == 0:
            print(self.count)

        if depth == 0:
            return self.get_score(board, player)
        elif has_win(board, player):
            return 1
        elif has_win(board, 1 - player):
            return -1
        else:
            moves = get_possibles_moves(board)
            s = max([-self.negamax(play_move_and_copy(board, move, player), depth - 1, 1 - player) for move in moves])
            return s

    def get_score(self, board: numpy.ndarray, player: int) -> float:
        return PoissonAI.get_score(board, player)
        return get_scores(board)[0][player]

        # def alphabeta(self, board: numpy.ndarray, depth: int, player: int, alpha: float, beta: float):
        #
        #     if depth == 0:
        #         return get_scores(board)[0][player]
        #     else:
        #         moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
        #         if len(moves) == 0:
        #             return get_scores(board)[0][player]
        #         else:
        #             u = -float('inf')
        #             for move in moves:
        #                 val = -self.alphabeta(self, play_move_and_copy(board, move[0], move[1], player), depth - 1,
        #                                       1 - player - alpha, -beta)
        #                 if val > u:
        #                     u = val
        #                     if u > alpha:
        #                         alpha = u
        #                         if alpha >= beta:
        #                             return u
        #             return u
