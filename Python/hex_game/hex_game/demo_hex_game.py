from hex_game.hex_game import HexGame


class DemoHexGame(HexGame):
    def play_move(self, x, y, player):
        self.board[x + 1, y + 1] = player
