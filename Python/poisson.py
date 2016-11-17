import numpy


class Poisson:
    def __init__(self, board):
        self.M = M = board.shape[0]
        self.N = N = self.M + 2

        self.C = -6 * numpy.ones((N, N))
        self.NE = numpy.ones((N, N))
        self.E = numpy.ones((N, N))
        self.SE = numpy.ones((N, N))
        self.NW = numpy.ones((N, N))
        self.SW = numpy.ones((N, N))
        self.W = numpy.ones((N, N))
        self.F = numpy.zeros((N, N))
        self.A = numpy.zeros((N, N))

        self.U = numpy.zeros((M, M))

        for i in range(M):
            for j in range(M):
                if board[i, j] != -1:
                    self.source_ponctuelle(i + 1, j + 1, [-1, 1][board[i, j]])

    def source_ponctuelle(self, x, y, v):
        self.C[x, y] = 1
        self.F[x, y] = v
        for K in [self.NE, self.E, self.SE, self.SW, self.W, self.NW]:
            K[x, y] = 0

    def norme(self):
        alpha = 0.01
        return numpy.sum(self.U > alpha) - numpy.sum(self.U < -alpha)

    def gauss_seidel(self):
        M = self.N - 1
        self.A[1:M, 1:M] = 1 / self.C[1:M, 1:M] * \
                           (self.F[1:M, 1:M] -
                            self.NE[1:M, 1:M] * self.A[1 - 1:M - 1, 1 + 1:M + 1] -
                            self.E[1:M, 1:M] * self.A[1:M, 1 + 1:M + 1] -
                            self.SE[1:M, 1:M] * self.A[1 + 1:M + 1, 1:M] -
                            self.SW[1:M, 1:M] * self.A[1 + 1:M + 1, 1 - 1:M - 1] -
                            self.W[1:M, 1:M] * self.A[1:M, 1 - 1:M - 1] -
                            self.NW[1:M, 1:M] * self.A[1 - 1:M - 1, 1:M])

    def iterations(self, ni):
        for i in range(ni):
            self.gauss_seidel()
        self.U = self.A[1:self.N - 1, 1:self.N - 1]
