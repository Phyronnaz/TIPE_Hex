import numpy as np

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QVBoxLayout

from hex_game.graphics.debug import Debug
from hex_game.graphics.ui_play import PlayUI
from hex_game.game import Game
from hex_game.graphics.mainwindow import Ui_TIPE
from hex_game.graphics.hex_view import HexView
from PyQt5 import QtCore, QtGui, QtWidgets
from hex_game.graphics.plot import MyDynamicMplCanvas, MyStaticMplCanvas


class UI:
    def __init__(self):
        # Variables

        # Window
        self.TIPE = QtWidgets.QMainWindow()
        self.Ui_TIPE = Ui_TIPE()
        self.Ui_TIPE.setupUi(self.TIPE)
        self.TIPE.show()

        # Subclasses
        self.playUI = PlayUI(self.Ui_TIPE)

        # Debug
        Debug.set_debug_play_text(self.Ui_TIPE.plainTextEditDebugPlay)


        # l = QVBoxLayout(self.Ui_TIPE.widget)
        # sc = MyStaticMplCanvas(self.Ui_TIPE.widget, width=5, height=4, dpi=100)
        # dc = MyDynamicMplCanvas(self.Ui_TIPE.widget, width=5, height=4, dpi=100)
        # l.addWidget(sc)
        # l.addWidget(dc)

        # Initial states

        # Connect actions
        self.Ui_TIPE.actionOpen.triggered.connect(self.open)
        self.Ui_TIPE.actionOpen.setShortcut("Ctrl+O")

        # Launch update functions

        # Set initial tab
        self.Ui_TIPE.tabWidget.setCurrentIndex(0)

    def open(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            for f in filenames:
                if f[len(f) - 6:len(f)] == ".model":
                    self.playUI.add_model(f)
