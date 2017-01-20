import numpy
from hex_game.main import NEIGHBORS_1


def init_winner_matrix_and_counter(size: int):
    """
    Init winner matrix and winner counter
    :param size: size of the board
    :return: winner_matrix, winner_counter
    """
    winner_matrix = numpy.zeros((size + 2, size + 2))
    winner_matrix[0, :] = -1
    winner_matrix[-1, :] = -2
    winner_matrix[:, 0] = 1
    winner_matrix[:, -1] = 2
    return winner_matrix, 3


def late_init_winner_matrix_and_counter(board: numpy.ndarray):
    """
       Init winner matrix and winner counter from already started board game
       :param board: board
       :return: winner_matrix, winner_counter
       """
    n = board.shape[0]
    winner_matrix, winner_counter = init_winner_matrix_and_counter(n)
    for i in range(n):
        for j in range(n):
            if board[i, j] != -1:
                _, winner_counter = check_for_winner((i, j), board[i, j], winner_matrix, winner_counter)
    return winner_matrix, winner_counter


def check_for_winner(move: (int, int), player: int, winner_matrix: numpy.ndarray, winner_counter: int) -> (int, int):
    """
    Process last move to check if last player won
    :param move: last move
    :param player: last player
    :param winner_matrix: winner_matrix
    :param winner_counter: winner_counter
    :return: winner, winner_counter
    """
    move = (move[0] + 1, move[1] + 1)  # translate move
    winner = -1
    p = 2 * player - 1  # -1 or 1

    # Find same team neighbors of the last move
    all_neighbors = [winner_matrix[move[0] + n[0], move[1] + n[1]] for n in NEIGHBORS_1]
    player_neighbors = numpy.unique([k for k in all_neighbors if k * p > 0])

    if len(player_neighbors) == 0:  # Last move alone
        winner_matrix[move] = winner_counter * p
        winner_counter += 1
    elif len(player_neighbors) == 1:  # Only one neighbors
        winner_matrix[move] = player_neighbors[0]
    elif 1 * p in player_neighbors and 2 * p in player_neighbors:  # if sides are now neighbors
        winner = player
    else:  # fusion groups
        m = min(abs(player_neighbors)) * p
        for k in player_neighbors:
            if k != m:
                winner_matrix[winner_matrix == k] = m
        winner_matrix[move] = m
    return winner, winner_counter
