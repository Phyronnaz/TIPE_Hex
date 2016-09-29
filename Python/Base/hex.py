import numpy as np


class Hex:
    def __init__(self, game):
        if game is None:
            self.game = np.zeros((11, 11))
        else:
            self.game = game
        self.winner = 0
        self.shape = 11

    def play_move(self, move, player):
        """
        Play move for player specified
        """
        x, y = move
        if 0 <= x < 11 and 0 <= y < 11 and self.game[x, y] == 0:
            self.game[x, y] = player
            return True
        else:
            return False

    def get_game_copy(self):
        return np.copy(self.game)

    def get_owner(self, x, y):
        return self.game[x, y]

    def get_winner(self):
        if (self.winner != 0):
            return self.winner
        else:
            def check(player):
                checked = np.zeros((11, 11), dtype=bool)
                pile = []
                for a in range(11):
                    if player == 1 and self.game[a, 0] == 1:
                        pile.append((a, 0))
                    elif player == 2 and self.game[0, a] == 2:
                        pile.append((0, a))

                while len(pile) != 0:
                    x, y = pile.pop()

                    if 0 <= x < 11 and 0 <= y < 11 and self.game[x, y] == player and not checked[x, y]:
                        if (x == 10 and player == 2) or (y == 10 and player == 1):
                            self.winner = player
                            return player

                        checked[x, y] = True
                        pile.append((x - 1, y))
                        pile.append((x + 1, y))
                        pile.append((x, y - 1))
                        pile.append((x, y + 1))
                        pile.append((x + 1, y - 1))
                        pile.append((x - 1, y + 1))

            check(1)
            check(2)

        return 0
