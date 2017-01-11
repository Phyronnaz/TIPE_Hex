import numpy
from tools import *
from hex_game import *


class Player:
    def __init__(self, model):
        self.model = model

    def play_move(self, player: int, board: numpy.ndarray) -> PlayerResponse:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: {move: Move, success: bool, message: string}
        """

        qval = self.model.predict(board.reshape(1, board.shape[0] - 2), batch_size=1)
        if random.random() < epsilon / 10:  # choose random action
            action = numpy.random.randint(0, 4)
        else:  # choose best action from Q(s,a) values
            action = numpy.argmax(qval)
        return action
        action = get_q_action(qval)
        move = action // size + 1, action % size + 1

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
