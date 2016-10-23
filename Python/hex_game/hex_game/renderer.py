import tkinter as tk

import numpy


class Renderer:
    def __init__(self, update_board=None, size: int = 11, scale: int = 25, rotation=numpy.pi / 6, debug_text=False):
        """
        Create new Renderer
        :param update_board: function to call to get the new board
        :param board: board to display
        :param scale: scale factor for tiles
        :param rotation: rotation of the board in radians
        """

        # Assign variables
        self.update_board = update_board
        self.size = size + 2
        self.scale = scale
        self.rotation = rotation
        self.click_delegates = []
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.x_offset = 0
        self.y_offset = 0

        # Initialize Tk and Canvas
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.focus_set()
        self.canvas.update()

        # Click
        def click(event):
            for f in self.click_delegates:
                f(event)

        self.canvas.bind("<Button-1>", click)

        # Initialize arrays
        self.polygons = []
        self.lines = []
        self.hexagons = numpy.zeros((self.size, self.size))

        # Create game hexagons
        for i in range(self.size):
            for j in range(self.size):
                self.hexagons[i][j] = self.create_hexagon(i, j, 'white', 0 != i != self.size - 1 != j != 0)

        # Recenter
        self.recenter()

        # Text
        if debug_text:
            for (p, l) in self.polygons:
                l = self.canvas.coords(p)
                x = l[::2]
                y = l[1::2]
                x = sum(x) / len(x)
                y = sum(y) / len(y)
                s = self.canvas.gettags(p)
                if 0 < int(s[0]) < self.size - 1 and 0 < int(s[1]) < self.size - 1:
                    self.canvas.create_text(x, y, text=s[0] + "," + s[1], state=tk.DISABLED, tag=s)

    def start(self):
        """
        Start loop
        """
        self.mainloop()
        self.window.mainloop()

    def clear_lines(self):
        for l in self.lines:
            self.canvas.delete(l)

    def create_line(self, p1, p2, color="yellow"):
        """
        Create line between p1 and p2
        :param p1: p1 in hex coordinate
        :param p2: p2 in hex coordinate
        :param color: color of the line
        """
        x1 = (2 * p1[0] + p1[1]) * numpy.sin(numpy.pi / 3)
        y1 = p1[1] * (2 - numpy.cos(5 * numpy.pi / 3))
        x2 = (2 * p2[0] + p2[1]) * numpy.sin(numpy.pi / 3)
        y2 = p2[1] * (2 - numpy.cos(5 * numpy.pi / 3))
        x1, y1 = self.get_coords(x1, y1)
        x2, y2 = self.get_coords(x2, y2)
        self.lines.append(self.canvas.create_line(x1, y1, x2, y2, state=tk.DISABLED, fill=color, width=self.scale / 5))

    def create_hexagon(self, x, y, fill_color, outline=True, transparent=False):
        """
        Create a hexagon on the canvas
        :param x:
        :param y:
        :param fill_color: string corresponding to the color of the polygon
        :param outline: outline or not
        :param transparent: transparent or not
        :return:
        """
        l = []
        for a in range(6):
            p_x = numpy.sin(a * numpy.pi / 3)
            p_y = numpy.cos(a * numpy.pi / 3)
            p_x += (2 * x + y) * numpy.sin(numpy.pi / 3)
            p_y += y * (2 - numpy.cos(5 * numpy.pi / 3))
            p_x, p_y = self.get_coords(p_x, p_y)
            l.append(p_x)
            l.append(p_y)

            self.min_x = min(self.min_x, p_x)
            self.min_y = min(self.min_y, p_y)
            self.max_x = max(self.max_x, p_x)
            self.max_y = max(self.max_y, p_y)

        o = 'black' if outline else ''
        t = str(x) + " " + str(y)
        s = "gray50" if transparent else ""
        p = self.canvas.create_polygon(l, outline=o, fill=fill_color, tag=t, stipple=s)
        self.polygons.append((p, l))
        return p

    def get_coords(self, x, y):
        """
        Convert coordinates
        :param x: x coordinate in hex game
        :param y: y coordinate in hex game
        :return: x, y coordinates in tkinter
        """
        r = numpy.array([[numpy.cos(self.rotation), -numpy.sin(self.rotation)],
                         [numpy.sin(self.rotation), numpy.cos(self.rotation)]])
        x *= self.scale
        y *= self.scale
        y, x = r.dot(numpy.array([x, y]))
        return x + self.x_offset, y + self.y_offset

    def recenter(self):
        """
        Recenter polygons
        """
        self.canvas.config(width=self.max_x - self.min_x, height=self.max_y - self.min_y)
        for (p, l) in self.polygons:
            m = [l[i] - (self.min_x if i % 2 == 0 else self.min_y) for i in range(len(l))]
            self.canvas.coords(p, *m)
        self.x_offset = -self.min_x
        self.y_offset = -self.min_y

    def mainloop(self):
        """
        Mainloop for tkinter
        """
        board = self.update_board() if self.update_board is not None else -numpy.ones((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                p = board[i, j]
                if i == 0 or i == self.size - 1:
                    c = '#99dafa'
                    ac = c
                elif j == 0 or j == self.size - 1:
                    c = '#f7597c'
                    ac = c
                elif p == -1:
                    c = 'white'
                    ac = 'grey'
                elif p == 0:
                    c = 'blue'
                    ac = 'cyan'
                elif p == 1:
                    c = 'red'
                    ac = 'pink'

                self.canvas.itemconfig(int(self.hexagons[i][j]), fill=c, activefill=ac)

        self.window.after(30, self.mainloop)
