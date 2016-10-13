import pyscreenshot

from hex_game.demo_hex_game import DemoHexGame
from hex_game.player_human import HumanPlayer
from hex_game.renderer import Renderer


class Demo:
    def __init__(self):
        self.player = HumanPlayer()
        self.hex_game = DemoHexGame()
        self.renderer = Renderer(self.update_delegate, self.hex_game)
        self.player.init(self.renderer)
        self.current_player = 0

        self.renderer.canvas.bind("<Tab>", self.change_player)
        self.renderer.canvas.bind("<space>", self.take_screenshot)
        self.renderer.start()

    def update_delegate(self):
        self.player.play_move(self.current_player, self.hex_game)

    def change_player(self, event):
        print("Changing player")
        self.current_player = (self.current_player + 2) % 3 - 1

    def take_screenshot(self, event):
        print("Taking screenshot")
        c = self.renderer.canvas
        box = c.winfo_rootx(), c.winfo_rooty(), c.winfo_rootx() + c.winfo_width(), c.winfo_rooty() + c.winfo_height()
        im = pyscreenshot.grab(bbox=box)
        im.show()
