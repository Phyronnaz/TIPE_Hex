from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import math
import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QTextBlockFormat, QTextCursor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem, QGraphicsLineItem, \
    QGraphicsSimpleTextItem


class HexView(QGraphicsView):
    def __init__(self, size, callback, *__args):
        QGraphicsView.__init__(self, *__args)
        self.size = size
        self.callback = callback
        self.scale = 20
        self.show_path = True
        self.colors = [Qt.green, Qt.yellow, Qt.black, Qt.cyan, Qt.magenta, Qt.gray]

        self.texts = []
        self.paths = {}
        self.paths_colors = {}
        self.polygons = np.zeros((size, size), dtype=object)
        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

        for i in range(-1, size + 1):
            for j in range(-1, size + 1):
                # Color
                if (i, j) in [(-1, -1), (-1, size), (size, -1), (size, size)]:
                    color = 'black'
                elif i in [-1, size]:
                    color = 'blue'
                elif j in [-1, size]:
                    color = 'red'
                else:
                    color = 'white'

                # Position
                x, y = self.position(i, j)

                tile = QGraphicsPolygonItemClick(x, y, size=self.scale, color=color,
                                                 callback=self.click, callback_args=(i, j))
                self.scene.addItem(tile)

                if color == 'white':
                    self.polygons[i, j] = tile
                    # Add text
                    text = self.scene.addText(str(i) + "," + str(j))
                    text.setPos(x - text.boundingRect().width() / 2, y - text.boundingRect().height() / 2)
                    self.texts.append(text)

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
        if 0 <= x < self.polygons.shape[0] > y >= 0:
            self.polygons[x, y].setColor(color)
        else:
            print("Out of bounds!")

    def set_path(self, path, id=None):
        if id is None:
            id = np.random.randint(1000000000)

        if id in self.paths:
            for arrow in self.paths[id]:
                self.scene.removeItem(arrow)
        else:
            self.paths_colors[id] = self.colors[len(self.paths)]

        l = []
        for i in range(1, len(path)):
            a = path[i - 1]
            b = path[i]
            start = self.position(*a)
            end = self.position(*b)
            arrow = Arrow(start, end, self.paths_colors[id])
            self.scene.addItem(arrow)
            l.append(arrow)

        self.paths[id] = l
        self.toggle_path(self.show_path)

    def clear_path(self):
        for id in self.paths:
            for arrow in self.paths[id]:
                self.scene.removeItem(arrow)
        self.paths.clear()

    def set_text(self, enabled):
        for text in self.texts:
            if enabled:
                text.show()
            else:
                text.hide()

    def toggle_path(self, enabled):
        self.show_path = enabled
        for id in self.paths:
            for arrow in self.paths[id]:
                if enabled:
                    arrow.show()
                else:
                    arrow.hide()

    def position(self, x, y):
        rotation = -np.pi / 6

        p_x = (2 * x + y) * np.sin(np.pi / 3)
        p_y = y * (2 - np.cos(5 * np.pi / 3))

        r = np.array([[np.cos(rotation), -np.sin(rotation)],
                      [np.sin(rotation), np.cos(rotation)]])

        p_y, p_x = r.dot(np.array([p_x, p_y]))

        p_x *= self.scale
        p_y *= self.scale

        return p_x, p_y


class QGraphicsPolygonItemClick(QGraphicsPolygonItem):
    def __init__(self, x, y, size, color, callback, callback_args):
        self.callback_args = callback_args
        self.callback = callback

        points = []
        for a in range(6):
            p_x = x + size * np.sin(a * np.pi / 3)
            p_y = y + size * np.cos(a * np.pi / 3)
            points.append(QPointF(p_x, p_y))

        polygon = QPolygonF(points)
        super().__init__(polygon)

        self.setPen(QPen(QColor("black"), size / 10))
        self.setBrush(QColor(color))

    def mousePressEvent(self, _):
        self.callback(*self.callback_args)

    def setColor(self, color):
        self.setBrush(QColor(color))

    def setColorRGB(self, r, g, b, a):
        self.setBrush(QColor(r, g, b, a))


class Arrow(QGraphicsLineItem):
    def __init__(self, start, end, color):
        super(Arrow, self).__init__(*start, *end)

        self.setPen(QPen(color, 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
