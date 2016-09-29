import numpy


class HexGame:
    def __init__(self, size=11, board=None):
        """
        Create new Hex Game
        :param board: Board to load
        :param size: Size of the game to create
        """
        self.board = board if board is not None else numpy.zeros((size, size))
        self.winner = 0
        self.size = size
        self.next_player = 1

    def play_move(self, move_x, move_y, player):
        """
        Make player play a move
        :param move_x: x position of the move
        :param move_y: y position of the move
        :param player: player whose playing
        :return: Whether or not the move succeed
        """
        if player == self.next_player and 0 <= move_x < self.size > move_y >= 0 and self.board[move_x, move_y] == 0:
            self.board[move_x, move_y] = player
            self.next_player = 3 - player
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
        :return: 0 if empty, 1 if owned by player 1 and else 2
        """
        return self.board[x, y]

    def get_winner(self):
        """
        Get the winner of the game
        :return: 0 if nobody win, 1 for player 1 and 2 for player 2
        """
        if self.winner == 0:
            if self.has_win(1):
                self.winner = 1
            elif self.has_win(2):
                self.winner = 2
        return self.winner

    def has_win(self, player):
        """
        Check if a player has win
        :param player: int corresponding to the player (1 or 2)
        :return: Whether or not player has win
        """
        checked = numpy.zeros(self.board.shape, dtype=bool)
        pile = []

        # Append edges
        for a in range(self.size):
            if player == 1 and self.board[a, 0] == 1:
                pile.append((a, 0))
            elif player == 2 and self.board[0, a] == 2:
                pile.append((0, a))

        # Process tiles
        while len(pile) != 0:
            x, y = pile.pop()

            if 0 <= x < self.size and 0 <= y < self.size and self.board[x, y] == player and not checked[x, y]:

                if (x == self.size - 1 and player == 2) or (y == self.size - 1 and player == 1):
                    return True

                checked[x, y] = True
                pile.append((x - 1, y))
                pile.append((x + 1, y))
                pile.append((x, y - 1))
                pile.append((x, y + 1))
                pile.append((x + 1, y - 1))
                pile.append((x - 1, y + 1))

        return False
