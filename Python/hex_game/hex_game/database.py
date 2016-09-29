import numpy as np

from hex_game.hex_game import HexGame

l = []

for i in range(100):
    h = HexGame(None)
    w = h.get_winner()
    j = 1

    while w == 0:
        w = h.get_winner()
        move = (np.random.randint(11), np.random.randint(11))
        j = (j + 1) % 2 + 1
        h.play_move(move, j)

    t = h.get_game()
    if j == 2:
        for i in range(11):
            for j in range(11):
                if t[i, j] == 1:
                    t[i, j] = 2
                elif [i, j] == 2:
                    t[i, j] = 1

    for i in range(11):
        for j in range(11):
            if [i, j] == 2:
                t[i, j] = 0

    l.append(t)

print(sum(l))
