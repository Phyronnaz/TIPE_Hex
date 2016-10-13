import random

import numpy

import hex_game.tools as tools
from hex_game.player import Player


class HumanPlayer(Player):
    def __init__(self):
        self.click_position = None

    def init(self, renderer):
        self.renderer = renderer
        self.renderer.click_delegate.append(self.callback)

    def play_move(self, player, hex_game):
        """
        Play a move
        :param player: Player playing
        :param hex_game: Hex Game to play on
        :return: 0 : fail, 1 :  success, 2 : wait
        """

        groups = [tools.get_groups(hex_game.board, k) for k in [0, 1]]
        # Debug groups and scores
        for k in [0, 1]:
            for g in groups[k]:
                color = "#" + ("%06x" % random.randint(0, 16777215))
                for c in g:
                    self.renderer.create_line(c[0] - numpy.ones(2), c[1] - numpy.ones(2), color)

        if self.click_position is None:
            return 2
        else:
            x, y = self.click_position
            self.click_position = None
            return 1 if hex_game.play_move(x, y, player) else 2

    def callback(self, event):
        id = event.widget.find_closest(event.x, event.y)
        s = self.renderer.canvas.gettags(id)
        if len(s) >= 2:
            self.click_position = int(s[0]), int(s[1])
