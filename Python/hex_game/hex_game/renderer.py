import tkinter as tk

import numpy


class Renderer:
    def __init__(self, update_delegate, hex_game, scale=25, rotation=45):
        """
        Create new Renderer
        :param update_delegate: function to call on update_delegate
        :param hex_game: Hex Game to display
        :param scale: scale factor for tiles
        :param rotation: rotation of the boad in degrees
        """

        # Assign variables
        self.update_delegate = update_delegate
        self.click_delegate = []
        self.hex_game = hex_game
        self.scale = scale
        self.rotation = rotation
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

        # Initialize Tk and Canvas
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.focus_set()
        self.canvas.update()

        # Click
        def click(event):
            for f in self.click_delegate:
                f(event)

        self.canvas.bind("<Button-1>", click)

        # Initialize arrays
        self.polygons = []
        self.hexagons = numpy.zeros(hex_game.board.shape)

        # Create game hexagons
        for i in range(hex_game.size):
            for j in range(hex_game.size):
                self.hexagons[i][j] = self.create_hexagon(i, j, 'white')

        # Create edges hexagons
        for x in range(-1, hex_game.size + 1):
            self.create_hexagon(x, -1, '#99dafa', False)
        for x in range(-1, hex_game.size + 1):
            self.create_hexagon(x, hex_game.size, '#99dafa', False)
        for y in range(-1, hex_game.size + 1):
            self.create_hexagon(-1, y, '#f7597c', False)
        for y in range(-1, hex_game.size + 1):
            self.create_hexagon(hex_game.size, y, '#f7597c', False)

        # Recenter
        self.canvas.config(width=self.max_x - self.min_x, height=self.max_y - self.min_y)
        for (p, l) in self.polygons:
            m = [l[i] - (self.min_x if i % 2 == 0 else self.min_y) for i in range(len(l))]
            self.canvas.coords(p, *m)

    def start(self):
        """
        Start looping
        """
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
        l = []
        for a in range(6):
            p_x = numpy.sin(a * numpy.pi / 3)
            p_y = numpy.cos(a * numpy.pi / 3)
            p_x += (2 * x + y) * numpy.sin(numpy.pi / 3)
            p_y += y * (2 - numpy.cos(5 * numpy.pi / 3))
            p_x *= self.scale
            p_y *= self.scale
            r = numpy.array([[numpy.cos(self.rotation), -numpy.sin(self.rotation)],
                             [numpy.sin(self.rotation), numpy.cos(self.rotation)]])
            p_x, p_y = r.dot(numpy.array([p_x, p_y]))
            l.append(p_x)
            l.append(p_y)

            self.min_x = min(self.min_x, p_x)
            self.min_y = min(self.min_y, p_y)
            self.max_x = max(self.max_x, p_x)
            self.max_y = max(self.max_y, p_y)

        o = 'black' if outline else ''
        t = str(x) + " " + str(y)
        p = self.canvas.create_polygon(l, outline=o, fill=fill_color, tag=t)
        self.polygons.append((p, l))
        return p

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
                    ac = 'grey'
                elif p == 1:
                    c = 'blue'
                    ac = 'cyan'
                elif p == 2:
                    c = 'red'
                    ac = 'pink'

                self.canvas.itemconfig(int(self.hexagons[i][j]), fill=c, activefill=ac)

        self.window.after(15, self.mainloop)
