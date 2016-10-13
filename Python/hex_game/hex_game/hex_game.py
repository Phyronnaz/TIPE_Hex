import numpy


class HexGame:
    def __init__(self, size=11, board=None):
        """
        Create new Hex Game
        :param board: Board to load
        :param size: Size of the game to create
        """
        self.board = board if board is not None else -numpy.ones((size + 2, size + 2))
        self.board[0, :] = 0
        self.board[-1, :] = 0
        self.board[:, -1] = 1
        self.board[:, 0] = 1
        self.winner = -1
        self.size = size
        self.next_player = 0

    def play_move(self, x, y, player):
        """
        Make player play a move
        :param x: x position of the move
        :param y: y position of the move
        :param player: player playing
        :return: Whether or not the move succeed
        """
        if 0 <= x < self.size > y >= 0 and self.board[x + 1, y + 1] == -1 and player == self.next_player:
            self.board[x + 1, y + 1] = player
            self.next_player = 1 - player
            return True
        else:
            return False

    def get_board_copy(self):
        """
        :return: Copy of the game board
        """
        return numpy.copy(self.board)

    def get_tile(self, x, y):
        """
        Get tile x, y
        :param x: x position
        :param y: y position
        :return: 0 if empty, 1 if owned by players 1 and else 2
        """
        return self.board[x + 1, y + 1]

    def get_winner(self):
        """
        Get the winner of the game
        :return: -1 if nobody win, 0 for players 0 and 1 for players 1
        """
        if self.winner == -1:
            if self.has_win(0):
                self.winner = 0
            elif self.has_win(1):
                self.winner = 1
        return self.winner

    def has_win(self, player):
        """
        Check if a player has win
        :param player: int corresponding to the player (0 or 1)
        :return: Whether or not player has win
        """
        checked = numpy.zeros((self.size, self.size), dtype=bool)
        pile = []

        # Append edges
        for a in range(self.size):
            if player == 0 and self.get_tile(0, a) == 0:
                pile.append((0, a))
            elif player == 1 and self.get_tile(a, 0) == 1:
                pile.append((a, 0))

        # Process tiles
        while len(pile) != 0:
            x, y = pile.pop()

            if 0 <= x < self.size and 0 <= y < self.size and self.get_tile(x, y) == player and not checked[x, y]:

                if (x == self.size - 1 and player == 0) or (y == self.size - 1 and player == 1):
                    return True

                checked[x, y] = True
                pile.append((x - 1, y))
                pile.append((x + 1, y))
                pile.append((x, y - 1))
                pile.append((x, y + 1))
                pile.append((x + 1, y - 1))
                pile.append((x - 1, y + 1))

        return False
