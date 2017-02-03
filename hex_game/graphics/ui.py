import numpy as np

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFileDialog

from game import Game
from graphics.mainwindow import Ui_TIPE
from graphics.hex_view import HexView
from PyQt5 import QtCore, QtGui, QtWidgets


class UI:
    def __init__(self, size):
        self.size = size
        self.game = None

        self.TIPE = QtWidgets.QMainWindow()
        hints = QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing | \
                QtGui.QPainter.SmoothPixmapTransform | QtGui.QPainter.TextAntialiasing
        self.Ui_TIPE = Ui_TIPE()

        self.Ui_TIPE.setupUi(self.TIPE)
        self.TIPE.show()

        self.Ui_TIPE.horizontalLayout.removeWidget(self.Ui_TIPE.graphicsViewDefault)
        self.Ui_TIPE.graphicsViewDefault.hide()
        self.Ui_TIPE.graphicsViewDefault = HexView(size, self.click, self.Ui_TIPE.centralWidget)
        self.Ui_TIPE.graphicsViewDefault.setEnabled(True)
        self.Ui_TIPE.graphicsViewDefault.setRenderHints(hints)
        self.Ui_TIPE.graphicsViewDefault.setObjectName("graphicsViewDefault")
        self.Ui_TIPE.horizontalLayout.addWidget(self.Ui_TIPE.graphicsViewDefault)

        self.Ui_TIPE.horizontalLayout.removeWidget(self.Ui_TIPE.graphicsViewPlayer1)
        self.Ui_TIPE.graphicsViewPlayer1.hide()
        self.Ui_TIPE.graphicsViewPlayer1 = HexView(size, self.click, self.Ui_TIPE.centralWidget)
        self.Ui_TIPE.graphicsViewPlayer1.setEnabled(True)
        self.Ui_TIPE.graphicsViewPlayer1.setRenderHints(hints)
        self.Ui_TIPE.graphicsViewPlayer1.setObjectName("graphicsViewPlayer1")
        self.Ui_TIPE.horizontalLayout.addWidget(self.Ui_TIPE.graphicsViewPlayer1)

        self.Ui_TIPE.horizontalLayout.removeWidget(self.Ui_TIPE.graphicsViewPlayer2)
        self.Ui_TIPE.graphicsViewPlayer2.hide()
        self.Ui_TIPE.graphicsViewPlayer2 = HexView(size, self.click, self.Ui_TIPE.centralWidget)
        self.Ui_TIPE.graphicsViewPlayer2.setEnabled(True)
        self.Ui_TIPE.graphicsViewPlayer2.setRenderHints(hints)
        self.Ui_TIPE.graphicsViewPlayer2.setObjectName("graphicsViewPlayer2")
        self.Ui_TIPE.horizontalLayout.addWidget(self.Ui_TIPE.graphicsViewPlayer2)

        self.Ui_TIPE.pushButtonPlay.setEnabled(False)

        self.Ui_TIPE.comboBoxPlayer1.activated.connect(self.update_combo_box)
        self.Ui_TIPE.comboBoxPlayer2.activated.connect(self.update_combo_box)

        self.Ui_TIPE.pushButtonViewDefault.clicked.connect(self.handle_view)
        self.Ui_TIPE.pushButtonViewPlayer1.clicked.connect(self.handle_view)
        self.Ui_TIPE.pushButtonViewPlayer2.clicked.connect(self.handle_view)

        self.Ui_TIPE.pushButtonPlay.clicked.connect(self.play_button)
        self.Ui_TIPE.pushButtonNewGame.clicked.connect(self.new_game)

        self.Ui_TIPE.actionLoad.triggered.connect(self.load)
        self.Ui_TIPE.actionLoad.setShortcut("Ctrl+O")

        self.models = []

        # Initial state
        self.Ui_TIPE.pushButtonViewDefault.setChecked(True)
        self.Ui_TIPE.pushButtonViewPlayer1.setChecked(False)
        self.Ui_TIPE.pushButtonViewPlayer2.setChecked(False)

        self.handle_view()
        self.set_progress_bar(-1)
        self.update_models()
        self.update_combo_box()

    def load(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.models += filenames
            self.update_models()

    def update_combo_box(self):
        if self.Ui_TIPE.comboBoxPlayer1.currentIndex() == 1:
            self.Ui_TIPE.labelMinimaxDepthPlayer1.show()
            self.Ui_TIPE.spinBoxMinimaxDepthPlayer1.show()
        else:
            self.Ui_TIPE.labelMinimaxDepthPlayer1.hide()
            self.Ui_TIPE.spinBoxMinimaxDepthPlayer1.hide()

        if self.Ui_TIPE.comboBoxPlayer2.currentIndex() == 1:
            self.Ui_TIPE.labelMinimaxDepthPlayer2.show()
            self.Ui_TIPE.spinBoxMinimaxDepthPlayer2.show()
        else:
            self.Ui_TIPE.labelMinimaxDepthPlayer2.hide()
            self.Ui_TIPE.spinBoxMinimaxDepthPlayer2.hide()

    def update_models(self):
        names = [m.split("/")[-1] for m in self.models]
        self.Ui_TIPE.listWidget.clear()
        self.Ui_TIPE.listWidget.addItems(names)

        self.Ui_TIPE.comboBoxPlayer1.clear()
        self.Ui_TIPE.comboBoxPlayer2.clear()
        players = ["Human", "Minimax", "Random"] + names
        self.Ui_TIPE.comboBoxPlayer1.addItems(players)
        self.Ui_TIPE.comboBoxPlayer2.addItems(players)

    def handle_view(self):
        if self.Ui_TIPE.pushButtonViewDefault.isChecked():
            self.Ui_TIPE.graphicsViewDefault.show()
        else:
            self.Ui_TIPE.graphicsViewDefault.hide()

        if self.Ui_TIPE.pushButtonViewPlayer1.isChecked():
            self.Ui_TIPE.graphicsViewPlayer1.show()
        else:
            self.Ui_TIPE.graphicsViewPlayer1.hide()

        if self.Ui_TIPE.pushButtonViewPlayer2.isChecked():
            self.Ui_TIPE.graphicsViewPlayer2.show()
        else:
            self.Ui_TIPE.graphicsViewPlayer2.hide()

    def set_progress_bar(self, value):
        if value >= 0:
            self.Ui_TIPE.progressBarMinimax.show()
            self.Ui_TIPE.progressBarMinimax.setValue(value)
        else:
            self.Ui_TIPE.progressBarMinimax.hide()

    def play_button(self):
        if self.game is not None:
            move = self.game.play()
            self.update_board()

    def click(self, x, y):
        if self.game is not None:
            self.game.click(x, y)
            self.update_board()

    def update_board(self):
        b = np.zeros(self.game.board.shape, dtype=object)
        for i in range(b.shape[0]):
            for j in range(b.shape[1]):
                v = self.game.board[i, j]
                b[i, j] = ["blue", "red", "white"][v]
        self.Ui_TIPE.graphicsViewDefault.set_board(b, rgb=False)

    def display_Q(self, player, values):
        if player == 1:
            values *= -1
        h = self.Ui_TIPE.graphicsViewPlayer1, self.Ui_TIPE.graphicsViewPlayer2
        h[player].set_board(self.get_board(values), rgb=True)

    def get_board(self, values):
        board = np.zeros(shape=values.shape, dtype=object)
        m = values.max()
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                r = 0 if values[i, j] < 0 else values[i, j] / m
                b = 0 if values[i, j] > 0 else values[i, j] / m
                board[i, j] = (r, 0, b)
        return board

    def new_game(self):
        c = self.Ui_TIPE.comboBoxPlayer1.currentText(), self.Ui_TIPE.comboBoxPlayer2.currentText()
        d = self.Ui_TIPE.spinBoxMinimaxDepthPlayer1.value(), self.Ui_TIPE.spinBoxMinimaxDepthPlayer2.value()
        players = [None, None]
        for i in range(2):
            if c[i] == "Human":
                players[i] = "Human", ""
            elif c[i] == "Minimax":
                players[i] = "Minimax", d[i]
            elif c[i] == "Random":
                players[i] = "Random", ""
            else:
                players[i] = "Q learning", c[i]
        self.game = Game(self.size, players, self.display_Q)
        self.Ui_TIPE.pushButtonPlay.setEnabled(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = UI(5)
    sys.exit(app.exec_())
