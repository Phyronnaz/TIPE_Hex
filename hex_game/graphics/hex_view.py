import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem


class HexView(QGraphicsView):
    def __init__(self, size, callback, *__args):
        QGraphicsView.__init__(self, *__args)
        self.size = size
        self.callback = callback
        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

        self.polygons = np.zeros((size, size), dtype=object)

        for i in range(-1, size + 1):
            for j in range(-1, size + 1):
                if (i, j) in [(-1, -1), (-1, size), (size, -1), (size, size)]:
                    color = 'black'
                elif i in [-1, size]:
                    color = 'blue'
                elif j in [-1, size]:
                    color = 'red'
                else:
                    color = 'white'
                item = QGraphicsPolygonItemClick(i, j, 25, -np.pi / 6, self.click, color=color)
                self.scene.addItem(item)
                if color == 'white':
                    self.polygons[i, j] = item

    def click(self, x, y):
        if 0 <= x < self.size > y >= 0:
            self.callback(x, y)

    def set_board(self, board):
        for i in range(self.size):
            for j in range(self.size):
                if board[i, j] == 0 or np.isnan(board[i, j]):
                    r, g, b, a = 0, 0, 0, 0
                elif board[i, j] < 0:
                    r, g, b, a = 255, 0, 0, -int(board[i, j] * 255)
                else:
                    r, g, b, a = 0, 0, 255, int(board[i, j] * 255)
                self.polygons[i, j].setColorRGB(r, g, b, a)

    def set_color(self, x, y, color):
        self.polygons[x, y].set_color(color)


class QGraphicsPolygonItemClick(QGraphicsPolygonItem):
    def __init__(self, x, y, size, rotation, callback, color):
        self.position = x, y
        self.callback = callback
        points = []
        for a in range(6):
            p_x = np.sin(a * np.pi / 3)
            p_y = np.cos(a * np.pi / 3)
            p_x += (2 * x + y) * np.sin(np.pi / 3)
            p_y += y * (2 - np.cos(5 * np.pi / 3))

            r = np.array([[np.cos(rotation), -np.sin(rotation)],
                          [np.sin(rotation), np.cos(rotation)]])
            p_x *= size
            p_y *= size
            p_y, p_x = r.dot(np.array([p_x, p_y]))

            points.append(QPointF(p_x, p_y))
        polygon = QPolygonF(points)
        super().__init__(polygon)
        self.setPen(QPen(QColor("black"), size / 10))
        self.setBrush(QColor(color))

    def mousePressEvent(self, _):
        self.callback(*self.position)

    def setColor(self, color):
        self.setBrush(QColor(color))

    def setColorRGB(self, r, g, b, a):
        self.setBrush(QColor(r, g, b, a))
