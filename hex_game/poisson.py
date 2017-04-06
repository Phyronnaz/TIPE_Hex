import numpy

from hex_game.main import NEIGHBORS_1, NEIGHBORS_2


class Poisson:
    def __init__(self, board, scales):
        self.m = m = board.shape[0]
        self.n = n = self.m + 4

        self.C = -6  * numpy.ones((n, n))

        self.F = numpy.zeros((n, n))
        self.A = numpy.zeros((n, n))

        U = numpy.zeros((m, m))

        for i in range(m):
            for j in range(m):
                if board[i, j] != -1:
                    self.source_ponctuelle(i + 2, j + 2, [-1, 1][board[i, j]] * scales[i, j])

    def source_ponctuelle(self, x, y, v):
        self.C[x, y] = 1
        self.F[x, y] = v

    def gauss_seidel(self):
        n = self.n
        A = self.A
        C = self.C
        F = self.F
        s = 2
        e = n - 2

        neighbors_1 = numpy.zeros((e - s, e - s))
        for (a, b) in NEIGHBORS_1:
            neighbors_1 += A[s + a:e + a, s + b:e + b]

        neighbors_2 = numpy.zeros((e - s, e - s))
        for (a, b) in NEIGHBORS_2:
            neighbors_2 += A[s + a:e + a, s + b:e + b]

        A[s:e, s:e] = 1 / C[s:e, s:e] * (F[s:e, s:e] - (F[s:e, s:e] == 0) * (neighbors_1 + 0 * neighbors_2))

    def iterations(self, ni):
        for i in range(ni):
            self.gauss_seidel()
        self.U = self.A[2:self.n - 2, 2:self.n - 2]
