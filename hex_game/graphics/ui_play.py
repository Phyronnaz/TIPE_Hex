import numpy as np
from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from hex_game.ai_poisson import get_path
from hex_game.game import Game
from hex_game.graphics import debug
from hex_game.graphics.hex_view import HexView
from hex_game.graphics.mainwindow import Ui_TIPE
from hex_game.main import invert_path
from hex_game.players import *
from hex_game.players.player_poisson import PoissonPlayer


class PlayUI:
    def __init__(self, ui: Ui_TIPE):
        debug.play_ui = self

        # Variables
        self.ui = ui
        self.size = -1
        self.game = None  # type: Game
        self.models_paths = []
        self.displayed_players = []

        # Players
        self.human = HumanPlayer()
        self.minimax = MinimaxPlayer()
        self.random = RandomPlayer()
        self.poisson = PoissonPlayer()
        self.players = [self.human, self.minimax, self.random, self.poisson]

        # Init
        self.init_ui()
        self.update_combobox()
        self.update_minimax_spinbox()
        self.update_size()

    def init_ui(self):
        # Initial states
        self.ui.pushButtonViewPlayer1.setChecked(False)
        self.ui.pushButtonViewPlayer2.setChecked(False)

        self.ui.pushButtonPlay.setEnabled(False)

        # Shortcuts
        self.shortcut_play = QShortcut(QKeySequence("Return"), self.ui.playTab)
        self.shortcut_play.activated.connect(self.play)

        # Connect actions
        self.ui.pushButtonScreenshot.clicked.connect(self.screenshot)

        self.ui.spinBoxSizePlay.valueChanged.connect(self.update_size)

        self.ui.comboBoxPlayer1.activated.connect(self.update_minimax_spinbox)
        self.ui.comboBoxPlayer2.activated.connect(self.update_minimax_spinbox)

        self.ui.pushButtonViewPlayer1.clicked.connect(self.update_graphics_views_visibility)
        self.ui.pushButtonViewPlayer2.clicked.connect(self.update_graphics_views_visibility)
        self.ui.pushButtonViewText.clicked.connect(self.update_text)
        self.ui.pushButtonViewPath.clicked.connect(self.toggle_path)

        self.ui.pushButtonPlay.clicked.connect(self.play)

        self.ui.pushButtonNewGame.clicked.connect(self.new_game)

    def reload_graphics_views(self):
        """
        Recreate HexViews
        """
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

    def update_size(self):
        """
        Apply size change
        """
        self.size = self.ui.spinBoxSizePlay.value()
        self.reload_graphics_views()
        self.update_graphics_views_visibility()
        self.game = None
        self.update_game()
        self.update_combobox()

    def update_minimax_spinbox(self):
        """
        Apply player change
        """
        if type(self.displayed_players[self.ui.comboBoxPlayer1.currentIndex()]) is MinimaxPlayer:
            self.ui.labelMinimaxDepthPlayer1.show()
            self.ui.spinBoxMinimaxDepthPlayer1.show()
        else:
            self.ui.labelMinimaxDepthPlayer1.hide()
            self.ui.spinBoxMinimaxDepthPlayer1.hide()

        if type(self.displayed_players[self.ui.comboBoxPlayer2.currentIndex()]) is MinimaxPlayer:
            self.ui.labelMinimaxDepthPlayer2.show()
            self.ui.spinBoxMinimaxDepthPlayer2.show()
        else:
            self.ui.labelMinimaxDepthPlayer2.hide()
            self.ui.spinBoxMinimaxDepthPlayer2.hide()

    def update_combobox(self):
        """
        Update list of the models and players choice
        """
        self.displayed_players = [k for k in self.players if k.check(self.size)]
        names = [k.name for k in self.displayed_players]

        text1 = self.ui.comboBoxPlayer1.currentText()
        text2 = self.ui.comboBoxPlayer2.currentText()

        self.ui.comboBoxPlayer1.clear()
        self.ui.comboBoxPlayer2.clear()

        self.ui.comboBoxPlayer1.addItems(names)
        self.ui.comboBoxPlayer2.addItems(names)

        self.ui.comboBoxPlayer1.setCurrentText(text1)
        self.ui.comboBoxPlayer2.setCurrentText(text2)

    def update_graphics_views_visibility(self):
        """
        Enable/Disable HexViews
        """
        if self.ui.pushButtonViewPlayer1.isChecked():
            self.ui.graphicsViewPlayer1.show()
        else:
            self.ui.graphicsViewPlayer1.hide()

        if self.ui.pushButtonViewPlayer2.isChecked():
            self.ui.graphicsViewPlayer2.show()
        else:
            self.ui.graphicsViewPlayer2.hide()

    def update_text(self):
        self.ui.graphicsViewDefault.set_text(self.ui.pushButtonViewText.isChecked())
        self.ui.graphicsViewPlayer1.set_text(self.ui.pushButtonViewText.isChecked())
        self.ui.graphicsViewPlayer2.set_text(self.ui.pushButtonViewText.isChecked())

    def toggle_path(self):
        self.ui.graphicsViewDefault.toggle_path(self.ui.pushButtonViewPath.isChecked())
        self.ui.graphicsViewPlayer1.toggle_path(self.ui.pushButtonViewPath.isChecked())
        self.ui.graphicsViewPlayer2.toggle_path(self.ui.pushButtonViewPath.isChecked())

    def update_game(self):
        """
        Update UI after a move
        """
        self.update_boards()
        b = self.game is not None and self.game.winner == -1 and self.game.players[self.game.player].name != "Human"
        self.ui.pushButtonPlay.setEnabled(b)

    def update_boards(self):
        """
        Update HexViews
        """
        if self.game is not None:
            aux1 = self.game.players[0].get_aux_board(self.game.board, 0)
            aux2 = self.game.players[1].get_aux_board(self.game.board, 1)
            self.ui.graphicsViewDefault.set_board(self.get_board(self.game.board, q=False))
            if aux1 is not None:
                self.ui.graphicsViewPlayer1.set_board(self.get_board(aux1, q=True))
                self.ui.graphicsViewPlayer1.set_texts(aux1)
            if aux2 is not None:
                self.ui.graphicsViewPlayer2.set_board(self.get_board(aux2, q=True))
                self.ui.graphicsViewPlayer2.set_texts(aux2)

            path = get_path(self.game.board, 1 - self.game.player)
            self.debug_path(invert_path(path, 1 - self.game.player), id=0, player=-1)

    def play(self):
        """
        Handle play button click
        """
        if self.game is not None and self.game.players[self.game.player].name != "Human":
            self.game.play()
            self.update_game()

    def click(self, x, y):
        """
        Handle a click on the tile with coordinate x y
        :param x: x
        :param y: y
        """
        if self.game is not None and self.game.players[self.game.player].name == "Human":
            self.human.move = x, y
            self.game.play()
            self.update_game()

    def get_board(self, board, q):
        """
        Convert a game board to a hex one
        :param board: board
        :param q: values between -1 and 1?
        :return: new board
        """
        t = np.zeros(shape=board.shape)
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if q:
                    t[i, j] = board[i, j]
                else:
                    if board[i, j] == -1:
                        t[i, j] = 0
                    elif board[i, j] == 0:
                        t[i, j] = 1
                    else:
                        t[i, j] = -1
        return t

    def screenshot(self):
        name = self.ui.lineEditScreenshotName.text()
        self.ui.graphicsViewDefault.screenshot(name + "_main")
        self.ui.graphicsViewPlayer1.screenshot(name + "_1")
        self.ui.graphicsViewPlayer2.screenshot(name + "_2")

    def new_game(self):
        """
        Create a new game
        """
        combos = self.ui.comboBoxPlayer1.currentIndex(), self.ui.comboBoxPlayer2.currentIndex()
        players = [self.displayed_players[combos[k]] for k in range(2)]
        self.game = Game(self.size, players)
        self.update_game()
        self.ui.graphicsViewDefault.clear_path()
        self.ui.graphicsViewPlayer1.clear_path()
        self.ui.graphicsViewPlayer2.clear_path()
        debug.debug_play("New Game")

    def add_model(self, path):
        """
        Add a model
        :param path: path of the model to add
        """
        if path not in self.models_paths:
            self.models_paths.append(path)
            self.players.append(QLearningPlayer(path))
            self.update_combobox()

    def debug_path(self, path, id=None, player=-1):
        if player == -1:
            self.ui.graphicsViewDefault.set_path(path, id)
        if player == 0:
            self.ui.graphicsViewPlayer1.set_path(path, id)
        if player == 1:
            self.ui.graphicsViewPlayer2.set_path(path, id)
