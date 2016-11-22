import pyscreenshot
from poisson import Poisson

from hex_game import *
from player_human import HumanPlayer
from renderer import Renderer


class Screenshot:
    def __init__(self, visual_size=11, debug_text=True):
        self.player = HumanPlayer()
        self.board = init_board(visual_size=visual_size)
        self.renderer = Renderer(update_board=self.update_delegate, visual_size=visual_size, debug_text=debug_text, scale=30)
        self.player.init(self.renderer)
        self.current_player = 0

        self.polygons = []
        self.poisson_enabled = False

        self.renderer.canvas.bind("<Tab>", self.change_player)
        self.renderer.canvas.bind("<space>", self.take_screenshot)
        self.renderer.canvas.bind("t", self.toggle_text)
        self.renderer.canvas.bind("p", self.toggle_poisson)
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

    def toggle_poisson(self, event):
        if self.poisson_enabled:
            for p in self.polygons:
                self.renderer.canvas.delete(p)
        else:
            self.poisson()
        self.poisson_enabled = not self.poisson_enabled

    def poisson(self):
        def hexa(f):
            s = str(hex(int(255 * f)))[2:]
            while len(s) < 2:
                s = "0" + s
            while len(s) > 2:
                s = s[:-1]
            return s

        poisson = Poisson(self.board)
        poisson.iterations(100)
        n = poisson.U.shape[0]
        for i in range(n):
            for j in range(n):
                c = "#" + hexa(max(0, poisson.U[i, j])) + "00" + hexa(-min(0, poisson.U[i, j]))
                self.polygons.append(self.renderer.create_hexagon(i, j, c, outline=False))
