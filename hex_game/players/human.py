import numpy


class HumanPlayer:
    def init(self, game):
        self.click_position = (-1, -1)
        self.game = game
        self.game.click_delegates.append(self.click)

    def get_move(self, player: int, board: numpy.ndarray) -> (int, int):
        move = self.click_position
        if self.click_position != (-1, -1):
            self.click_position = (-1, -1)
        return move

    def click(self, event):
        id = event.widget.find_closest(event.x, event.y)
        s = self.game.canvas.gettags(id)
        if len(s) >= 2:
            self.click_position = int(s[0]) - 1, int(s[1]) - 1
