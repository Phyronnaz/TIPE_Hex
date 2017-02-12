import numpy as np

from hex_game.graphics.debug import Debug
from hex_game.game import Game
from hex_game.graphics.hex_view import HexView
from PyQt5 import QtGui


class PlayUI:
    def __init__(self, Ui_TIPE):
        # Variables
        self.size = -1
        self.game = None
        self.models = []

        self.Ui_TIPE = Ui_TIPE

        # Initial states
        self.Ui_TIPE.pushButtonViewDefault.setChecked(True)
        self.Ui_TIPE.pushButtonViewPlayer1.setChecked(False)
        self.Ui_TIPE.pushButtonViewPlayer2.setChecked(False)

        self.Ui_TIPE.pushButtonPlay.setEnabled(False)

        # Connect actions
        self.Ui_TIPE.spinBoxSize.valueChanged.connect(self.update_size)

        self.Ui_TIPE.comboBoxPlayer1.activated.connect(self.update_combo_box)
        self.Ui_TIPE.comboBoxPlayer2.activated.connect(self.update_combo_box)

        self.Ui_TIPE.pushButtonViewDefault.clicked.connect(self.update_graphics_views)
        self.Ui_TIPE.pushButtonViewPlayer1.clicked.connect(self.update_graphics_views)
        self.Ui_TIPE.pushButtonViewPlayer2.clicked.connect(self.update_graphics_views)

        self.Ui_TIPE.pushButtonPlay.clicked.connect(self.play_button)
        self.Ui_TIPE.pushButtonPlay.setShortcut("Return")
        self.Ui_TIPE.pushButtonNewGame.clicked.connect(self.new_game)

        # Launch update functions
        self.update_progress_bar(-1)
        self.update_models_list()
        self.update_combo_box()
        self.update_size()

    def reload_graphics_views(self):
        hints = QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing | \
                QtGui.QPainter.SmoothPixmapTransform | QtGui.QPainter.TextAntialiasing

        self.Ui_TIPE.horizontalLayoutPlayTab.removeWidget(self.Ui_TIPE.graphicsViewDefault)
        self.Ui_TIPE.horizontalLayoutPlayTab.removeWidget(self.Ui_TIPE.graphicsViewPlayer1)
        self.Ui_TIPE.horizontalLayoutPlayTab.removeWidget(self.Ui_TIPE.graphicsViewPlayer2)

        self.Ui_TIPE.graphicsViewDefault.deleteLater()
        self.Ui_TIPE.graphicsViewPlayer1.deleteLater()
        self.Ui_TIPE.graphicsViewPlayer2.deleteLater()

        self.Ui_TIPE.graphicsViewDefault = HexView(self.size, self.click, self.Ui_TIPE.playTab)
        self.Ui_TIPE.graphicsViewPlayer1 = HexView(self.size, self.click, self.Ui_TIPE.playTab)
        self.Ui_TIPE.graphicsViewPlayer2 = HexView(self.size, self.click, self.Ui_TIPE.playTab)

        self.Ui_TIPE.graphicsViewDefault.setEnabled(True)
        self.Ui_TIPE.graphicsViewPlayer1.setEnabled(True)
        self.Ui_TIPE.graphicsViewPlayer2.setEnabled(True)

        self.Ui_TIPE.graphicsViewDefault.setRenderHints(hints)
        self.Ui_TIPE.graphicsViewPlayer1.setRenderHints(hints)
        self.Ui_TIPE.graphicsViewPlayer2.setRenderHints(hints)

        self.Ui_TIPE.graphicsViewDefault.setObjectName("graphicsViewDefault")
        self.Ui_TIPE.graphicsViewPlayer1.setObjectName("graphicsViewPlayer1")
        self.Ui_TIPE.graphicsViewPlayer2.setObjectName("graphicsViewPlayer2")

        self.Ui_TIPE.horizontalLayoutPlayTab.addWidget(self.Ui_TIPE.graphicsViewDefault)
        self.Ui_TIPE.horizontalLayoutPlayTab.addWidget(self.Ui_TIPE.graphicsViewPlayer1)
        self.Ui_TIPE.horizontalLayoutPlayTab.addWidget(self.Ui_TIPE.graphicsViewPlayer2)

    def add_model(self, filename):
        if filename not in self.models:
            self.models.append(filename)
            self.update_models_list()

    def update_size(self):
        self.size = self.Ui_TIPE.spinBoxSize.value()
        self.reload_graphics_views()
        self.update_graphics_views()
        self.game = None
        self.update_game()

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

    def update_models_list(self):
        names = [m.split("/")[-1] for m in self.models]

        self.Ui_TIPE.listWidgetModels.clear()
        self.Ui_TIPE.listWidgetModels.addItems(names)

        self.Ui_TIPE.comboBoxPlayer1.clear()
        self.Ui_TIPE.comboBoxPlayer2.clear()

        players = ["Human", "Minimax", "Random"] + names

        self.Ui_TIPE.comboBoxPlayer1.addItems(players)
        self.Ui_TIPE.comboBoxPlayer2.addItems(players)

    def update_graphics_views(self):
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

    def update_progress_bar(self, value):
        if value >= 0:
            self.Ui_TIPE.progressBarMinimax.show()
            self.Ui_TIPE.progressBarMinimax.setValue(value)
        else:
            self.Ui_TIPE.progressBarMinimax.hide()

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
        self.Ui_TIPE.pushButtonPlay.setEnabled(b)

    def update_boards(self):
        if self.game is not None:
            self.Ui_TIPE.graphicsViewDefault.set_board(self.get_board(self.game.board, q=False))
            self.Ui_TIPE.graphicsViewPlayer1.set_board(self.get_board(self.game.aux_boards[0], q=True))
            self.Ui_TIPE.graphicsViewPlayer2.set_board(self.get_board(-self.game.aux_boards[1], q=True))

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
        combos = self.Ui_TIPE.comboBoxPlayer1.currentIndex(), self.Ui_TIPE.comboBoxPlayer2.currentIndex()
        depths = self.Ui_TIPE.spinBoxMinimaxDepthPlayer1.value(), self.Ui_TIPE.spinBoxMinimaxDepthPlayer2.value()
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
        Debug.debug_play("New Game")
