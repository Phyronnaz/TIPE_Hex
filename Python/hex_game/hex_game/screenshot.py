import numpy
import pyscreenshot

import hex_game.hex_game as hex
from hex_game.player_human import HumanPlayer
from hex_game.renderer import Renderer


class Screenshot:
    def __init__(self, size=11):
        self.player = HumanPlayer()
        self.board = hex.init_board(size=size)
        self.renderer = Renderer(update_board=self.update_delegate, size=size, debug_text=True)
        self.player.init(self.renderer)
        self.current_player = 0

        self.renderer.canvas.bind("<Tab>", self.change_player)
        self.renderer.canvas.bind("<space>", self.take_screenshot)
        self.renderer.start()

    def update_delegate(self):
        board = -numpy.ones(self.board.shape)
        self.player.play_move(self.current_player, board)
        i, j = max(numpy.argmax(board, axis=0)), max(numpy.argmax(board, axis=1))
        self.board[i, j] = self.current_player
        return self.board

    def change_player(self, event):
        print("Changing player")
        self.current_player = (self.current_player + 2) % 3 - 1

    def take_screenshot(self, event):
        print("Taking screenshot")
        c = self.renderer.canvas
        box = c.winfo_rootx(), c.winfo_rooty(), c.winfo_rootx() + c.winfo_width(), c.winfo_rooty() + c.winfo_height()
        im = pyscreenshot.grab(bbox=box)
        im.show()
