from hex_game import *


class Player:
    def play_move(self, player: int, board: numpy.ndarray) -> PlayerResponse:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :return: {move: Move, success: bool, message: string}
        """
        trial_count = 0
        has_played = False
        visual_size = board.shape[0] - 2

        x = numpy.random.randint(visual_size) + 1
        y = numpy.random.randint(visual_size) + 1

        move = (x, y)

        while not has_played and trial_count <= visual_size ** 2:
            move = (move[0] % visual_size + 1, move[1] % visual_size + 1)
            trial_count += 1
            has_played = play_move(board, move, player)

        return {'move': move, 'success': has_played, 'message': ""}
