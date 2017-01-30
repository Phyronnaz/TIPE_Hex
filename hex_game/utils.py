import numpy


def get_splitted_board(board, player):
    if player == 1:
        board = board.T
    size = board.shape[0]
    t = numpy.zeros((3, size, size))
    t[0] = board == 0
    t[1] = board == 1 + player
    t[2] = board == 2 - player
    return t.reshape(1, size ** 2 * 3)
