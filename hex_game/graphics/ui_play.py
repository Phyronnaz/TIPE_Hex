import numpy as np
from hex_game import hex_io
from hex_game.graphics import debug
from hex_game.game import Game
from hex_game.graphics.hex_view import HexView
from PyQt5 import QtGui
from hex_game.graphics.mainwindow import Ui_TIPE


class PlayUI:
    def __init__(self, ui: Ui_TIPE):
        # Variables
        self.size = -1
        self.game = None
        self.models = []

        self.ui = ui

        # Initial states
        self.ui.pushButtonViewDefault.setChecked(True)
        self.ui.pushButtonViewPlayer1.setChecked(False)
        self.ui.pushButtonViewPlayer2.setChecked(False)

        self.ui.pushButtonPlay.setEnabled(False)

        # Connect actions
        self.ui.spinBoxSizePlay.valueChanged.connect(self.update_size)

        self.ui.comboBoxPlayer1.activated.connect(self.update_combo_box)
        self.ui.comboBoxPlayer2.activated.connect(self.update_combo_box)

        self.ui.pushButtonViewDefault.clicked.connect(self.update_graphics_views)
        self.ui.pushButtonViewPlayer1.clicked.connect(self.update_graphics_views)
        self.ui.pushButtonViewPlayer2.clicked.connect(self.update_graphics_views)

        self.ui.pushButtonPlay.clicked.connect(self.play_button)
        self.ui.pushButtonPlay.setShortcut("Return")
        self.ui.pushButtonNewGame.clicked.connect(self.new_game)

        # Launch update functions
        self.update_progress_bar(-1)
        self.update_models_list()
        self.update_combo_box()
        self.update_size()

    def reload_graphics_views(self):
        hints = QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing | \
                QtGui.QPainter.SmoothPixmapTransform | QtGui.QPainter.TextAntialiasing

        self.ui.horizontalLayoutPlayTab.removeWidget(self.ui.graphicsViewDefault)
        self.ui.horizontalLayoutPlayTab.removeWidget(self.ui.graphicsViewPlayer1)
        self.ui.horizontalLayoutPlayTab.removeWidget(self.ui.graphicsViewPlayer2)

        self.ui.graphicsViewDefault.deleteLater()
        self.ui.graphicsViewPlayer1.deleteLater()
        self.ui.graphicsViewPlayer2.deleteLater()

        self.ui.graphicsViewDefault = HexView(self.size, self.click, self.ui.playTab)
        self.ui.graphicsViewPlayer1 = HexView(self.size, self.click, self.ui.playTab)
        self.ui.graphicsViewPlayer2 = HexView(self.size, self.click, self.ui.playTab)

        self.ui.graphicsViewDefault.setEnabled(True)
        self.ui.graphicsViewPlayer1.setEnabled(True)
        self.ui.graphicsViewPlayer2.setEnabled(True)

        self.ui.graphicsViewDefault.setRenderHints(hints)
        self.ui.graphicsViewPlayer1.setRenderHints(hints)
        self.ui.graphicsViewPlayer2.setRenderHints(hints)

        self.ui.graphicsViewDefault.setObjectName("graphicsViewDefault")
        self.ui.graphicsViewPlayer1.setObjectName("graphicsViewPlayer1")
        self.ui.graphicsViewPlayer2.setObjectName("graphicsViewPlayer2")

        self.ui.horizontalLayoutPlayTab.addWidget(self.ui.graphicsViewDefault)
        self.ui.horizontalLayoutPlayTab.addWidget(self.ui.graphicsViewPlayer1)
        self.ui.horizontalLayoutPlayTab.addWidget(self.ui.graphicsViewPlayer2)

    def add_model(self, filename):
        if filename not in self.models:
            self.models.append(filename)
            self.update_models_list()

    def update_size(self):
        self.size = self.ui.spinBoxSizePlay.value()
        self.reload_graphics_views()
        self.update_graphics_views()
        self.game = None
        self.update_game()
        self.update_models_list()

    def update_combo_box(self):
        if self.ui.comboBoxPlayer1.currentIndex() == 1:
            self.ui.labelMinimaxDepthPlayer1.show()
            self.ui.spinBoxMinimaxDepthPlayer1.show()
        else:
            self.ui.labelMinimaxDepthPlayer1.hide()
            self.ui.spinBoxMinimaxDepthPlayer1.hide()

        if self.ui.comboBoxPlayer2.currentIndex() == 1:
            self.ui.labelMinimaxDepthPlayer2.show()
            self.ui.spinBoxMinimaxDepthPlayer2.show()
        else:
            self.ui.labelMinimaxDepthPlayer2.hide()
            self.ui.spinBoxMinimaxDepthPlayer2.hide()

    def update_models_list(self):
        names = [m.split("/")[-1] for m in self.models]

        self.ui.listWidgetModels.clear()
        self.ui.listWidgetModels.addItems(names)

        players = ["Human", "Minimax", "Random"] + [n for n in names if hex_io.get_parameters(n)[0] == self.size]

        self.ui.comboBoxPlayer1.clear()
        self.ui.comboBoxPlayer2.clear()

        self.ui.comboBoxPlayer1.addItems(players)
        self.ui.comboBoxPlayer2.addItems(players)

    def update_graphics_views(self):
        if self.ui.pushButtonViewDefault.isChecked():
            self.ui.graphicsViewDefault.show()
        else:
            self.ui.graphicsViewDefault.hide()

        if self.ui.pushButtonViewPlayer1.isChecked():
            self.ui.graphicsViewPlayer1.show()
        else:
            self.ui.graphicsViewPlayer1.hide()

        if self.ui.pushButtonViewPlayer2.isChecked():
            self.ui.graphicsViewPlayer2.show()
        else:
            self.ui.graphicsViewPlayer2.hide()

    def update_progress_bar(self, value):
        if value >= 0:
            self.ui.progressBarMinimax.show()
            self.ui.progressBarMinimax.setValue(value)
        else:
            self.ui.progressBarMinimax.hide()

    def play_button(self):
        if self.game is not None:
            self.game.play()
            self.update_game()

    def click(self, x, y):
        if self.game is not None:
            self.game.click(x, y)
            self.update_game()

    def update_game(self):
        self.update_boards()
        b = self.game is not None and self.game.winner == -1 and self.game.players[self.game.player][0] != "Human"
        self.ui.pushButtonPlay.setEnabled(b)

    def update_boards(self):
        if self.game is not None:
            self.ui.graphicsViewDefault.set_board(self.get_board(self.game.board, q=False))
            self.ui.graphicsViewPlayer1.set_board(self.get_board(self.game.aux_boards[0], q=True))
            self.ui.graphicsViewPlayer2.set_board(self.get_board(-self.game.aux_boards[1], q=True))

    @staticmethod
    def get_board(board, q):
        t = np.zeros(shape=board.shape)
        m = abs(board).max() if abs(board).max() != 0 else 1
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if q:
                    t[i, j] = board[i, j] / m
                else:
                    if board[i, j] == -1:
                        t[i, j] = 0
                    elif board[i, j] == 0:
                        t[i, j] = 1
                    else:
                        t[i, j] = -1
        return t

    def new_game(self):
        combos = self.ui.comboBoxPlayer1.currentIndex(), self.ui.comboBoxPlayer2.currentIndex()
        depths = self.ui.spinBoxMinimaxDepthPlayer1.value(), self.ui.spinBoxMinimaxDepthPlayer2.value()
        players = [None, None]
        for i in range(2):
            if combos[i] == 0:
                players[i] = "Human", ""
            elif combos[i] == 1:
                players[i] = "Minimax", depths[i]
            elif combos[i] == 2:
                players[i] = "Random", ""
            else:
                players[i] = "Q learning", self.models[combos[i] - 3]
        self.game = Game(self.size, players)
        self.update_game()
        debug.debug_play("New Game")
