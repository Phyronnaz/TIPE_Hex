from player import Player
from poisson import Poisson
from hex_game import *
import random
from tools import *
import numpy

Path = List[Position]


class PoissonAI(Player):
    def init(self, renderer):
        pass

    def play_move(self, player: int, board: numpy.ndarray) -> int:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        # densities, paths = self.get_path(board, player)
        # l = numpy.array([densities[k] for k in paths])
        # # TODO: check if path emtpy
        # try:
        #     move = paths[numpy.argmin(l)]
        # except ValueError:
        #     print("!!!!!!!!!!!!!!!!!!!!!!")
        #     print("!!!!Empty response!!!!")
        #     print("!!!Playing randomly!!!")
        #     print("!!!!!!!!!!!!!!!!!!!!!!")
        #     move = random.choice([k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0])
        moves = [k for k in numpy.argwhere(board == -1) if 0 != k[0] != board.shape[0] != k[1] != 0]
        move = moves[numpy.argmax(
            [PoissonAI.get_score(play_move_copy(board, moves[i][0], moves[i][1], player), player) for i in
             range(len(moves))])]
        print("Poisson move: " + str(move))
        return play_move(board, move[0], move[1], player)

    @staticmethod
    def get_norme(board):
        poisson = Poisson(board)
        poisson.iterations(board.shape[0] * 5)
        return poisson.norme()

    @staticmethod
    def get_path(board: numpy.ndarray, player: int) -> Tuple[numpy.ndarray, Path]:
        n = board.shape[0]
        matrix = numpy.zeros(board.shape, dtype=float)
        paths = [[[] for _ in range(n)] for _ in range(n)]
        poisson = Poisson(board)
        poisson.iterations(board.shape[0] * 5)
        U = poisson.U * [-1, 1][player]
        for a in range(n - 1):
            for b in range(n - 1):
                x, y = (a, b) if player == 0 else (b, a)
                if board[x, y] == 1 - player:
                    matrix[x, y] = -float('inf')
                else:
                    if player == 0 and y != 0:
                        if x == 0:
                            matrix[x, y] = U[x, y]
                            paths[x][y] = [(x, y)]
                        else:
                            if y == 11:
                                m = (x - 1, y)
                            else:
                                i = numpy.argmax([U[x - 1, y], U[x - 1, y + 1]])
                                m = (x - 1, y) if i == 0 else (x - 1, y + 1)
                            matrix[x, y] = matrix[m] + U[x, y]
                            paths[x][y] = paths[m[0]][m[1]] + [(x, y)]
                    elif player == 1 and x != 0:
                        if y == 0:
                            matrix[x, y] = U[x, y]
                            paths[x][y] = [(x, y)]
                        else:
                            if x == 11:
                                m = (x, y - 1)
                            else:
                                i = numpy.argmax([U[x, y - 1], U[x + 1, y - 1]])
                                m = (x, y - 1) if i == 0 else (x + 1, y - 1)
                            matrix[x, y] = matrix[m] + U[x, y]
                            paths[x][y] = paths[m[0]][m[1]] + [(x, y)]
        f = lambda i: ((i, n - 2) if player == 1 else (n - 2, i))
        max_i = numpy.argmax([matrix[f(i)] for i in range(n)])
        return U, paths[f(max_i)[0]][f(max_i)[1]]

    @staticmethod
    def get_score(board: numpy.ndarray, player: int) -> int:
        densities, paths = PoissonAI.get_path(board, player)
        l = numpy.array([densities[k] for k in paths])
        return l.min()
        # return l.sum()
        # return l.sum()   - l.std()
