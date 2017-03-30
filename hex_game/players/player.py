import numpy


class Player:
    size = 0
    name = ""

    def get_move(self, board: numpy.ndarray, player: int):
        pass

    def get_aux_board(self, board: numpy.ndarray, player: int):
        pass

    def check(self, size):
        return True
