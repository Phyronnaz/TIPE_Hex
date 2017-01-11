import numpy
from hex_game import play_move_and_copy, get_possibles_moves
from winner_check import late_init_winner_matrix_and_counter, check_for_winner


def get_move_negamax(board: numpy.ndarray, player: int, depth: int):
    winner_matrix, winner_counter = late_init_winner_matrix_and_counter(board)

    moves = get_possibles_moves(board)
    scores = len(moves) * [0]
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
        print("Move {}: Score {}".format(moves[i], scores[i]))
    return moves[numpy.argmax(scores)]


def negamax(board: numpy.ndarray, winner_matrix: numpy.ndarray, winner_counter: int, depth: int, player: int) -> float:
    if depth == 0:
        return 0  # score

    moves = get_possibles_moves(board)
    scores = len(moves) * [0]
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
