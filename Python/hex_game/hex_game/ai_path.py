from hex_game.player import Player


class PathAI:
    def __init__(self):
        self.human = Player()

    def init(self, renderer):
        self.renderer = renderer
        self.human.init(renderer)

    def play_move(self, player, hex_game):
        """
        Play a move
        :param player: Player playing
        :param hex_game: Hex Game to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """
        self.detect_paths(hex_game.board, player - 1)
        return self.human.play_move(player, hex_game)

    def detect_paths(self, board, player):
        positions = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] == player:
                    positions.append((i, j))
        couples = []
        for p1 in positions:
            x = p1[0]
            y = p1[1]
            l = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
            l += [(x - 1, y - 1), (x - 2, y + 1), (x - 1, y + 2), (x + 1, y + 1), (x + 2, y - 1), (x + 1, y - 2)]
            for p2 in l:
                if 0 <= p2[0] < board.shape[0] and 0 <= p2[1] < board.shape[1]:
                    # self.renderer.create_hexagon(p2[0], p2[1], "pink", transparent=True)
                    if board[p2] == player:
                        couples.append((p1, p2))
        for c in couples:
            self.renderer.create_line(c[0], c[1])
