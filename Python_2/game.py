import tkinter
import numpy
from hex_game import play_move, can_play_move, init_board, has_win


class ResizingCanvas(tkinter.Canvas):
    def __init__(self, parent, size, **kwargs):
        tkinter.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.relative_scale = min(self.winfo_height() / size, self.winfo_width() / 1.5 / size) * 200

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        scale = float(event.width) / self.width
        self.width = event.width
        self.height = event.height

        self.relative_scale *= scale

        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, scale, scale)


class Game:
    def __init__(self, size, player0, player1, rotation=numpy.pi / 6, rate=10):
        """
        Create new Renderer
        :param size: size of the board
        :param rotation: rotation of the board in radians
        """

        # Assign variables
        self.real_size = size + 2
        self.rotation = rotation
        self.click_delegates = []
        self.players = [player0, player1]
        self.rate = rate

        # Initialize Tk and Canvas
        self.master = tkinter.Tk()
        self.canvas = ResizingCanvas(self.master, self.real_size)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.canvas.focus_set()
        self.canvas.update()

        self.x_offset = self.canvas.relative_scale
        self.y_offset = self.canvas.relative_scale

        # Click
        def click(event):
            for f in self.click_delegates:
                f(event)

        self.canvas.bind("<Button-1>", click)

        # Restart
        def restart(event):
            self.canvas.destroy()
            self.master.destroy()
            self.__init__(size, player0, player1, rotation, rate)
            self.start()

        self.canvas.bind("r", restart)

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
                color = 'blue' if i in [0, self.real_size - 1] else ('red' if j in [0, self.real_size - 1] else 'white')
                self.hexagons_array[i][j] = self.create_hexagon(i, j, color, outline=outline, board_hexagon=True)

        # Init game
        self.board = init_board(size)
        self.current_player = 0
        self.winner = -1

    def start(self):
        self.master.after(self.rate, self.update)
        tkinter.mainloop()

    def update(self):
        if self.winner == -1:
            p = self.current_player
            move = self.players[p].get_move(p, self.board)
            if can_play_move(self.board, move):
                play_move(self.board, move, p)
                self.winner = p if has_win(self.board, p) else -1
                self.current_player = (self.current_player + 1) % 2
                self.set_board(self.board, white=True)
        self.master.after(self.rate, self.update)

    def set_board(self, board, white=False):
        """
        Print board. White if player0 = 0 and player1 = 1 (else player0 = -1 and player1 = 1)
        """
        if white:
            for i in range(1, self.real_size - 1):
                for j in range(1, self.real_size - 1):
                    p = board[i - 1, j - 1]
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
                    self.canvas.itemconfig(int(self.hexagons_array[i + 1][j + 1]), fill=c, activefill=c)

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

        arrow = tkinter.LAST if arrow else tkinter.NONE

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
