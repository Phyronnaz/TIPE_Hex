import numpy
from tools import *
from hex_game import *


class Player:
    def __init__(self, state=None):
        self.state = numpy.random.RandomState() if state is None else state

    def play_move(self, player: int, board: numpy.ndarray) -> PlayerResponse:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: {move: Move, success: bool, message: string}
        """
        has_played = False

        moves = get_possibles_moves(board)
        self.state.random.shuffle(moves)

        move = None
        for m in moves:
            has_played = can_play_move(board, m)
            if has_played:
                move = m
                break

        message = "Playing randomly"

        return {'move': move, 'success': has_played, 'message': message}
