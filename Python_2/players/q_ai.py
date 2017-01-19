import numpy


class QPlayer:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def get_splitted_board(board):
        size = board.shape[0]
        t = numpy.zeros((3, size, size))
        t[0] = board == 0
        t[1] = board == 1
        t[2] = board == 2
        return t.reshape(1, size ** 2 * 3)

    def get_move(self, player: int, board: numpy.ndarray) -> (int, int):
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        """

        size = board.shape[0]

        qval = self.model.predict(self.get_splitted_board(board), batch_size=1)
        action = numpy.argmax(qval)

        move = action // size, action % size
        print("Q AI played at " + str(move))
        return move
