import random
from .renderer import Renderer
from .poisson import Poisson
from .tools import *


class Debug:
    debug_groups = True
    debug_poisson = True
    debug_indices = True
    debug_text = True

    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.polygons = []

    def update(self):
        self.renderer.clear_lines()
        self.renderer.clear_hexagons()
        if Debug.debug_groups:
            self.display_groups()
        if Debug.debug_poisson:
            self.display_poisson()
        if Debug.debug_indices:
            self.renderer.show_texts()
        else:
            self.renderer.hide_texts()

        class_name = str(type(self.players[self.next_player]).__name__)
        print(class_name + " (Player " + str(self.next_player) + ") played")
        print("New Scores:", get_scores(self.board)[0])
        if self.poisson_enabled:
            self.toggle_poisson()
            self.toggle_poisson()
        print("///////////////////////////")
        self.next_player = 1 - self.next_player

        print("Player " + str(self.winner) + " won")

    def display_groups(self):
        groups = [get_groups(self.board, k) for k in [0, 1]]
        for k in [0, 1]:
            for g in groups[k]:
                color = "#" + ("%06x" % random.randint(0, 16777215))
                for c in g:
                    self.renderer.create_line(c[0], c[1], color)

    def display_poisson(self):
        def hexa(f):
            s = str(hex(int(255 * f)))[2:]
            while len(s) < 2:
                s = "0" + s
            while len(s) > 2:
                s = s[:-1]
            return s

        poisson = Poisson(self.board)
        poisson.iterations(self.board.shape[0] * 5)
        n = poisson.U.shape[0]
        for i in range(n):
            for j in range(n):
                c = "#" + hexa(max(0, poisson.U[i, j])) + "00" + hexa(-min(0, poisson.U[i, j]))
                self.renderer.create_hexagon(i, j, c, outline=False)

    def start_text(self):
        if Debug.debug_text:
            print("///////////////////////////")
            print("Game Started")
            print("///////////////////////////")

    def update_text(self, player: int, winner: int, player_response):
        pass

