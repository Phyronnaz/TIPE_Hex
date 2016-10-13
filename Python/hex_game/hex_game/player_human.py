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
