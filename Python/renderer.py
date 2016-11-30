import tkinter as tk
import numpy
from resizing_canvas import ResizingCanvas


class Renderer:
    def __init__(self, visual_size: int = 11, rotation=numpy.pi / 6):
        """
        Create new Renderer
        :param visual_size: size of the board
        :param rotation: rotation of the board in radians
        """

        # Assign variables
        self.real_size = visual_size + 2
        self.rotation = rotation
        self.click_delegates = []

        # Initialize Tk and Canvas
        self.master = tk.Tk()
        self.canvas = ResizingCanvas(self.master, self.real_size)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.focus_set()
        self.canvas.update()

        self.x_offset = self.canvas.relative_scale
        self.y_offset = self.canvas.relative_scale

        # Click
        def click(event):
            for f in self.click_delegates:
                f(event)

        self.canvas.bind("<Button-1>", click)

        # Initialize arrays
        self.texts = []
        self.board_hexagons = []
        self.hexagons = []
        self.lines = []
        self.hexagons_array = numpy.zeros((self.real_size, self.real_size))

        # Create game hexagons
        s = self.real_size
        for i in range(self.real_size):
            for j in range(self.real_size):
                outline = 0 != i != self.real_size - 1 != j != 0
                self.hexagons_array[i][j] = self.create_hexagon(i, j, 'white', outline=outline, board_hexagon=True)

    def set_board(self, board, white=False):
        """
        Print board. White if player0 = 0 and player1 = 1 (else player0 = -1 and player1 = 1)
        """
        if white:
            for i in range(self.real_size):
                for j in range(self.real_size):
                    p = board[i, j]
                    if i == 0 or i == self.real_size - 1:
                        c = '#99dafa'
                        ac = c
                    elif j == 0 or j == self.real_size - 1:
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

                    self.canvas.itemconfig(int(self.hexagons_array[i][j]), fill=c, activefill=ac)
        else:
            def hexa(f):
                s = str(hex(int(255 * f)))[2:]
                while len(s) < 2:
                    s = "0" + s
                while len(s) > 2:
                    s = s[:-1]
                return s

            n = board.shape[0]

            for i in range(n):
                for j in range(n):
                    c = "#" + hexa(max(0, board[i, j])) + "00" + hexa(-min(0, board[i, j]))
                    self.canvas.itemconfig(int(self.hexagons_array[i][j]), fill=c, activefill=c)

    def create_line(self, p1, p2, color="black", arrow=False):
        """
        Create line between p1 and p2
        :param p1: p1 in hex coordinate
        :param p2: p2 in hex coordinate
        :param color: color of the line
        :param arrow: display arrow
        """

        l1 = self.canvas.coords(int(self.hexagons_array[p1]))
        l2 = self.canvas.coords(int(self.hexagons_array[p2]))

        x1 = sum(l1[::2]) / len(l1[::2])
        x2 = sum(l2[::2]) / len(l2[::2])

        y1 = sum(l1[1::2]) / len(l1[1::2])
        y2 = sum(l2[1::2]) / len(l2[1::2])

        arrow = tk.LAST if arrow else tk.NONE

        self.lines.append(self.canvas.create_line(x1, y1, x2, y2, state=tk.DISABLED, fill=color,
                                                  width=5, arrow=arrow, arrowshape=(13, 13, 7)))

    def create_hexagon(self, x, y, fill_color, outline=True, transparent=False, board_hexagon=False):
        """
        Create a hexagon on the canvas
        :param x:
        :param y:
        :param fill_color: string corresponding to the color of the polygon
        :param outline: outline or not
        :param transparent: transparent or not
        :param board_hexagon: wether or not this hexagon is part of the board
        :return:
        """
        if not board_hexagon:
            l = self.canvas.coords(int(self.hexagons_array[x, y]))
        else:
            l = []
            for a in range(6):
                p_x = numpy.sin(a * numpy.pi / 3)
                p_y = numpy.cos(a * numpy.pi / 3)
                p_x += (2 * x + y) * numpy.sin(numpy.pi / 3)
                p_y += y * (2 - numpy.cos(5 * numpy.pi / 3))
                p_x, p_y = self.get_coords(p_x, p_y)
                l.append(p_x)
                l.append(p_y)

        o = 'black' if outline else ''
        t = str(x) + " " + str(y) + " all"
        s = "gray50" if transparent else ""
        p = self.canvas.create_polygon(l, outline=o, fill=fill_color, tag=t, stipple=s)
        if board_hexagon:
            self.board_hexagons.append((p, l))
        else:
            self.hexagons.append((p, l))
        return p

    def clear_lines(self):
        """
        Delete all lines
        """
        for l in self.lines:
            self.canvas.delete(l)

    def clear_hexagons(self):
        """
           Delete all hexagons (except board ones)
       """
        for (p, l) in self.hexagons:
            self.canvas.delete(p)

    def show_texts(self):
        """
        Show cases indices
        """
        if len(self.texts) == 0:
            for (p, l) in self.board_hexagons:
                l = self.canvas.coords(p)
                x = l[::2]
                y = l[1::2]
                x = sum(x) / len(x)
                y = sum(y) / len(y)
                s = self.canvas.gettags(p)
                if 0 < int(s[0]) < self.real_size - 1 and 0 < int(s[1]) < self.real_size - 1:
                    self.texts.append(self.canvas.create_text(x, y, text=s[0] + "," + s[1], state=tk.DISABLED, tag=s))

    def hide_texts(self):
        """
        Hide cases indices
        """
        for t in self.texts:
            self.canvas.delete(t)
        self.texts.clear()

    def get_coords(self, x, y):
        """
        Convert coordinates
        :param x: x coordinate in hex game
        :param y: y coordinate in hex game
        :return: x, y coordinates in tkinter
        """
        # self.scale *= self.canvas.relative_scale
        r = numpy.array([[numpy.cos(self.rotation), -numpy.sin(self.rotation)],
                         [numpy.sin(self.rotation), numpy.cos(self.rotation)]])
        x *= self.canvas.relative_scale
        y *= self.canvas.relative_scale
        y, x = r.dot(numpy.array([x, y]))
        return x + self.x_offset, y + self.y_offset
