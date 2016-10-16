import hex_game.tools as tools
from hex_game.hex_game import HexGame
from hex_game.renderer import Renderer


class ToolsTest:
    def __init__(self):
        self.x = [1, 0]
        self.hex = HexGame()
        self.r = Renderer(self.update, self.hex)
        self.r.canvas.bind("q", lambda event: self.change([0, -1]))
        self.r.canvas.bind("z", lambda event: self.change([-1, 0]))
        self.r.canvas.bind("d", lambda event: self.change([0, 1]))
        self.r.canvas.bind("s", lambda event: self.change([1, 0]))
        self.r.start()

    def update(self):
        if self.x is not None:
            p = tools.get_next(self.x, self.hex.board, (5, 5), False)
            self.r.create_hexagon(p[0], p[1], "pink", transparent=True)
            self.x = None

    def change(self, x):
        self.x = x


ToolsTest()
