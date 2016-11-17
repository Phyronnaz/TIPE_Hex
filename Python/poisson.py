import numpy


class Poisson:
    def __init__(self, board):
        self.N = N = board.shape[0]

        self.C = 6 * numpy.ones((N, N))
        self.NE = numpy.ones((N, N))
        self.E = numpy.ones((N, N))
        self.SE = numpy.ones((N, N))
        self.SW = numpy.ones((N, N))
        self.W = numpy.ones((N, N))
        self.NW = numpy.ones((N, N))

        for i in range(N):
            for j in range(N):
                self.source_ponctuelle(i, j, [-1, 1, 0][board[i, j]])

    def source_ponctuelle(self, x, y, v):
        self.C[x, y] = 1
        self.F[x, y] = v
        for K in [self.NE, self.E, self.SE, self.SW, self.W, self.NW]:
            K[x, y] = 0

    def norme(self):
        return numpy.linalg.norm(self.U) / self.N ** 2

    def gauss_seidel(self):
        M = self.N - 1
        self.U[1:M, 1:M] = 1 / self.C[1:M, 1:M] * \
                           (self.F[1:M, 1:M] -
                            self.NE[1:M, 1:M] * self.U[1 - 1:M - 1, 1 + 1:M + 1] -
                            self.E[1:M, 1:M] * self.U[1:M, 1 + 1:M + 1] -
                            self.SE[1:M, 1:M] * self.U[1 + 1:M + 1, 1:M] -
                            self.SW[1:M, 1:M] * self.U[1 + 1:M + 1, 1 - 1:M - 1] -
                            self.W[1:M, 1:M] * self.U[1:M, 1 - 1:M - 1] -
                            self.NW[1:M, 1:M] * self.U[1 - 1:M - 1, 1:M])

    def iterations(self, ni):
        for i in range(ni):
            self.gauss_seidel()
