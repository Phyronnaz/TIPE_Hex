import tkinter as tk
import numpy as np


class Renderer():

    def __init__(self, update, hexGame):
        def create_polygon(i, j, fill, outline):
            p = 25
            l = []
            for a in range(6):
                x = np.sin(a * np.pi / 3)
                y = np.cos(a * np.pi / 3)
                x += (2 * i + j) * np.sin(np.pi / 3) + 5
                y += j * (2 - np.cos(5 * np.pi / 3)) + 5
                x *= p
                y *= p
                l.append(x)
                l.append(y)

            return self.canvas.create_polygon(l, outline=outline, fill=fill)

        self.update = update
        self.hex = hexGame

        # Initialize Tk and Canvas
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=900, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.focus_set()
        self.canvas.update()

        self.polygons = np.zeros((11, 11))

        for i in range(11):
            for j in range(11):
                self.polygons[i][j] = create_polygon(i, j, 'white', 'black')

        for x in range(-1, 12):
            create_polygon(x, -1, '#99dafa', '')
        for x in range(-1, 12):
            create_polygon(x, 11, '#99dafa', '')
        for y in range(-1, 12):
            create_polygon(-1, y, '#f7597c', '')
        for y in range(-1, 12):
            create_polygon(11, y, '#f7597c', '')

        self.mainLoop()
        self.window.mainloop()

    def mainLoop(self):
        self.update()
        for i in range(11):
            for j in range(11):
                p = self.hex.get_owner(i, j)
                if p == 0:
                    c = 'white'
                elif p == 1:
                    c = 'blue'
                elif p == 2:
                    c = 'red'

                self.canvas.itemconfig(int(self.polygons[i][j]), fill=c)

        self.window.after(1, self.mainLoop)
