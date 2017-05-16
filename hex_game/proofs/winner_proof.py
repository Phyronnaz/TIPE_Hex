from hex_game.main import get_random_move
from hex_game.main import play_move, init_board, has_win
from hex_game.winner_check import check_for_winner, init_winner_matrix_and_counter

size = 5

error = 0
n = 1000

for i in range(n):
    if i % 10 == 0:
        print(i)
    board = init_board(size)
    winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
    w = False
    p = 0
    while not w:
        move = get_random_move(board)
        play_move(board, move, p)
        hw = has_win(board, p)
        winner, winner_counter = check_for_winner(move, p, winner_matrix, winner_counter)
        w = hw or winner != -1
        if (not hw and winner != -1) or (hw and winner == -1):
            error += 1
        p = (p + 1) % 2

print("{} games played".format(n))
print("{} % of the games are ok".format((n - error) * 100 / n))
