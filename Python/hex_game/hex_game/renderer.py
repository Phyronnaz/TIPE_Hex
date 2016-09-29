import tkinter as tk

import numpy as np


class Renderer():
    def __init__(self, update_delegate, hex_game, width=900, height=600):
        """
        Create new Renderer
        :param update_delegate: function to call on update_delegate
        :param hex_game: Hex Game to display
        :param width: width of the window
        :param height: height of the window
        """

        # Assign variables
        self.update_delegate = update_delegate
        self.hex_game = hex_game

        # Initialize Tk and Canvas
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.focus_set()
        self.canvas.update()

        self.polygons = np.zeros(hex_game.board.shape)

        # Create game hexagons
        for i in range(hex_game.size):
            for j in range(hex_game.size):
                self.polygons[i][j] = self.create_hexagon(i, j, 'white')

        # Create edges hexagons
        for x in range(-1, 12):
            self.create_hexagon(x, -1, '#99dafa', '')
        for x in range(-1, 12):
            self.create_hexagon(x, 11, '#99dafa', '')
        for y in range(-1, 12):
            self.create_hexagon(-1, y, '#f7597c', '')
        for y in range(-1, 12):
            self.create_hexagon(11, y, '#f7597c', '')

        self.mainloop()
        self.window.mainloop()

    def create_hexagon(self, x, y, fill_color, outline=True):
        """
        Create a hexagon on the canvas
        :param x:
        :param y:
        :param fill_color: string corresponding to the color of the polygon
        :param outline: outline or not
        :return:
        """
        size_multiplier = 25
        l = []
        for a in range(6):
            p_x = np.sin(a * np.pi / 3)
            p_y = np.cos(a * np.pi / 3)
            p_x += (2 * x + y) * np.sin(np.pi / 3) + 5
            p_y += y * (2 - np.cos(5 * np.pi / 3)) + 5
            p_x *= size_multiplier
            p_y *= size_multiplier
            l.append(p_x)
            l.append(p_y)

        return self.canvas.create_polygon(l, outline='black' if outline else '', fill=fill_color)

    def mainloop(self):
        """
        Mainloop for tkinter
        """
        self.update_delegate()
        for i in range(self.hex_game.size):
            for j in range(self.hex_game.size):
                p = self.hex_game.get_tile(i, j)
                if p == 0:
                    c = 'white'
                elif p == 1:
                    c = 'blue'
                elif p == 2:
                    c = 'red'

                self.canvas.itemconfig(int(self.polygons[i][j]), fill=c)

        self.window.after(1, self.mainloop)
