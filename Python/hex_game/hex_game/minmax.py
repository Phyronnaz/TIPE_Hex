import numpy as np


def minmax(board, depth, play_move, get_score, get_moves, player, root_player):
    """

    :param board: numpy array
    :param depth: int
    :param play_move: param : board, player, move -> board
    :param get_score: param : board, -> score player0 - score player1
    :param get_moves: param : board, player -> tuple list
    :return: score player0-score player1
    """
    if depth > 0:
        moves = get_moves(board, player)
        scores = np.zeros(len(moves))

        for i in range(len(moves)):
            new_board = play_move(board, player, moves[i])
            score = minmax(new_board, depth - 1, play_move, get_score, get_moves, 1 - player, root_player)
            scores[i] = score[root_player] - score[1 - root_player]

        return max(scores)
    else:
        return get_score(board)
