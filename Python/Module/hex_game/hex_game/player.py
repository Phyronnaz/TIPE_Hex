from .hex_game import *


class Player:
    def init(self, renderer):
        pass

    def play_move(self, player: int, board: numpy.ndarray) -> bool:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        tries_count = 0
        has_played = False
        size = board.shape[0] - 2
        while not has_played and tries_count < size ** 2:
            tries_count += 1
            x = numpy.random.randint(size)
            y = numpy.random.randint(size)
            has_played = play_move(board, x + 1, y + 1, player)

        return has_played
