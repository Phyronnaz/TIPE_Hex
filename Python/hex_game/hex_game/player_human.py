import numpy

import hex_game.hex_game as hex
from hex_game.player import Player


class HumanPlayer(Player):
    def __init__(self):
        self.click_position = None
        self.renderer = None

    def init(self, renderer):
        self.renderer = renderer
        self.renderer.click_delegates.append(self.callback)

    def play_move(self, player: int, board: numpy.ndarray, cheat: bool = False) -> bool:
        """
        Play a move
        :param player: Player playing
        :param board: board to play on
        :param cheat: allow to play everywhere
        :return: 0 : fail, 1 :  success, 2 : wait
        """

        if self.click_position is None:
            return 2
        else:
            x, y = self.click_position
            self.click_position = None
            if cheat:
                board[x, y] = player
                return 1
            else:
                return 1 if hex.play_move(board, x, y, player) else 2

    def callback(self, event):
        id = event.widget.find_closest(event.x, event.y)
        s = self.renderer.canvas.gettags(id)
        if len(s) >= 2:
            self.click_position = int(s[0]), int(s[1])
