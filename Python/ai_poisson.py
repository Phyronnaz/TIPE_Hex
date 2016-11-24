from player import Player
from poisson import Poisson
from debug import Debug
from tools import *
import numpy
import random


class PoissonAI(Player):
    def play_move(self, player: int, board: numpy.ndarray) -> PlayerResponse:
        densities, paths = self.get_path(board, player)
        l = numpy.array([densities[k] for k in paths])
        # TODO: check if path emtpy
        try:
            message = "Playing minimum of the path"
            move = paths[numpy.argmin(l)]
        except ValueError:
            message = Debug.FAIL + "Empty response. Playing randomly!"
            possibles_moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
            move = tuple(random.choice(possibles_moves))
        # moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
        # move = moves[numpy.argmax(
        #     [PoissonAI.get_score(play_move_and_copy(board, moves[i], player), player) for i in
        #      range(len(moves))])]
        return {'move': move, 'success': True, 'message': message}

    @staticmethod
    def get_norme(board):
        poisson = Poisson(board)
        poisson.iterations(board.shape[0] * 5)
        return poisson.norme()

    @staticmethod
    def get_path(board: numpy.ndarray, player: int) -> Tuple[numpy.ndarray, Path]:
        n = board.shape[0]
        board = board if player == 0 else board.T

        weights = numpy.zeros(board.shape, dtype=float)
        paths = [[[] for _ in range(n)] for _ in range(n)]

        poisson = Poisson(board)
        poisson.iterations(board.shape[0] * 5)
        U = poisson.U * [-1, 1][player]  # player cases > 0

        def try_to_update(x: int, y: int):
            down = [(x - 1, y)] if y == 11 else [(x - 1, y), (x - 1, y + 1)]
            sides = [(x, y - 1), (x, y + 1)]
            l = sides + down
            i = numpy.argmax([weights[l[i]] for i in range(len(l))])
            old_weight = weights[x, y]
            m = l[i]
            weights[x, y] = U[x, y] + weights[m]
            paths[x][y] = [(x, y)] + paths[m[0]][m[1]]
            return old_weight == weights[x, y]

        for x in range(1, n - 1):
            has_changed = True
            while has_changed:
                has_changed = False
                for y in range(1, n - 1):
                    if board[x, y] == 1 - player:
                        weights[x, y] = -float('inf')
                    else:
                        if x == 1:
                            weights[x, y] = U[x, y]
                            paths[x][y] = [(x, y)]
                        else:
                            has_changed = not try_to_update(x, y)
        max_i = numpy.argmax([weights[(n - 2, i)] for i in range(n)])
        return U, paths[n - 2][max_i]

    @staticmethod
    def get_score(board: numpy.ndarray, player: int) -> int:
        densities, paths = PoissonAI.get_path(board, player)
        l = numpy.array([densities[k] for k in paths])
        return l.min()
        # return l.sum()
        # return l.sum()   - l.std()
