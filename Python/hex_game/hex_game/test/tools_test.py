import hex_game.hex_game as hex
import hex_game.tools as tools
from hex_game.renderer import Renderer


class ToolsTest:
    def __init__(self):
        self.side = None
        self.board = hex.init_board()
        self.renderer = Renderer(self.update, self.board, debug_text=True)
        self.renderer.canvas.bind("<Left>", lambda event: self.change([0, -1]))
        self.renderer.canvas.bind("<Up>", lambda event: self.change([-1, 0]))
        self.renderer.canvas.bind("<Right>", lambda event: self.change([0, 1]))
        self.renderer.canvas.bind("<Down>", lambda event: self.change([1, 0]))
        self.renderer.canvas.bind("c", lambda event: self.clear())
        self.renderer.start()

    def update(self):
        self.board[5, 5] = 0
        if self.side is not None:
            p = tools.get_next(self.side, (5, 5), True)
            if p is not None:
                self.board[p[0], p[1]] = 1
            else:
                print("Error")
            self.side = None
        return self.board

    def change(self, side):
        self.side = side

    def clear(self):
        self.board = hex.init_board()


ToolsTest()
