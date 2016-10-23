import pyscreenshot

import hex_game.hex_game as hex
from hex_game.player_human import HumanPlayer
from hex_game.renderer import Renderer


class Screenshot:
    def __init__(self, size=11):
        self.player = HumanPlayer()
        self.board = hex.init_board(size=size)
        self.renderer = Renderer(update_board=self.update_delegate, size=size)
        self.player.init(self.renderer)
        self.current_player = 0

        self.renderer.canvas.bind("<Tab>", self.change_player)
        self.renderer.canvas.bind("<space>", self.take_screenshot)
        self.renderer.canvas.bind("t", self.toggle_text)
        self.index = 0
        self.text = False
        self.renderer.click_delegates.append(self.create_text)

        self.renderer.start()

    def update_delegate(self):
        self.player.play_move(self.current_player, self.board, cheat=True)
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

    def create_text(self, event):
        if self.text:
            id = event.widget.find_closest(event.x, event.y)
            l = self.renderer.canvas.coords(id)
            l_x = l[::2]
            l_y = l[1::2]
            x = sum(l_x) / len(l_x)
            y = sum(l_y) / len(l_y)
            self.renderer.canvas.create_text(x, y, text=str(self.index))
            self.index += 1
            self.text = False

    def toggle_text(self, event):
        self.text = not self.text
