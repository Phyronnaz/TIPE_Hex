import numpy as np

import os
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout

from hex_game.graphics.ui_train import TrainUI
from hex_game.graphics.ui_results import ResultsUI
from hex_game.graphics import debug
from hex_game.graphics.ui_play import PlayUI
from hex_game.game import Game
from hex_game.graphics.mainwindow import Ui_TIPE
from hex_game.graphics.hex_view import HexView
from PyQt5 import QtCore, QtGui, QtWidgets


class UI:
    def __init__(self):
        # Window
        self.TIPE = QtWidgets.QMainWindow()
        self.ui = Ui_TIPE()
        self.ui.setupUi(self.TIPE)
        self.TIPE.setWindowTitle("TIPE Hex")
        self.TIPE.show()

        # Subclasses
        self.playUI = PlayUI(self.ui)
        self.resultsUI = ResultsUI(self.ui)
        self.tainUI = TrainUI(self.ui)

        # Debug
        self.ui.plainTextEditDebugPlay.clear()
        debug.debug_play_text = self.ui.plainTextEditDebugPlay

        # Connect actions
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionOpen.setShortcut("Ctrl+O")

        # Launch update functions

        # Set initial tab
        self.ui.tabWidget.setCurrentIndex(0)

    def open(self):
        if self.ui.tabWidget.currentIndex() == 0:
            filter = "Model (*.model);;Stats (*.hdf5)"
        else:
            filter = "Stats (*.hdf5);;Model (*.model)"

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter(filter)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            for f in fileNames:
                if os.path.exists(f):
                    if dialog.selectedNameFilter() == "Model (*.model)":
                        self.playUI.add_model(f)
                    else:
                        self.resultsUI.add_result(f)
                elif f != "":
                    msgBox = QMessageBox()
                    msgBox.setText("File does not exist")
                    msgBox.setWindowTitle("Error")
                    msgBox.exec_()
