###############################
# Fichier qui gère le minimax #
###############################

from hex_game.main import *
from hex_game.winner_check import *
import numpy as np


def get_move_negamax(board: numpy.ndarray, player: int, depth: int) -> (int, int):
    """
    Get move from negamax
    :param board: board
    :param player: player
    :param depth: depth
    :return: move
    """
    winner_matrix, winner_counter = late_init_winner_matrix_and_counter(board)

    moves = get_possibles_moves(board)
    scores = np.zeros(len(moves))
    values = numpy.zeros(board.shape)

    for i in range(len(moves)):
        wm = numpy.copy(winner_matrix)
        new_board = play_move_and_copy(board, moves[i], player)
        winner, wc = check_for_winner(moves[i], player, wm, winner_counter)

        if winner == -1:
            scores[i] = -negamax(new_board, wm, wc, depth - 1, 1 - player)
        elif winner == player:
            scores[i] = float('inf')
        else:
            scores[i] = -float('inf')
        values[moves[i]] = scores[i]
    return moves[numpy.argmax(scores)], values


def negamax(board: numpy.ndarray, winner_matrix: numpy.ndarray, winner_counter: int, depth: int, player: int) -> float:
    """
    Recursive negamax
    :param board: board
    :param winner_matrix: winner matrix 
    :param winner_counter: winner counter
    :param depth: depth
    :param player: player
    :return: score
    """
    if depth == 0:
        return 0  # score

    moves = get_possibles_moves(board)
    scores = np.zeros(len(moves))

    for i in range(len(moves)):
        new_board = play_move_and_copy(board, moves[i], player)
        wm = numpy.copy(winner_matrix)
        winner, winner_counter = check_for_winner(moves[i], player, wm, winner_counter)

        if winner == -1:
            scores[i] = -negamax(new_board, wm, winner_counter, depth - 1, 1 - player)
        elif winner == player:
            return 1
        else:
            return -1

    return max(scores)
