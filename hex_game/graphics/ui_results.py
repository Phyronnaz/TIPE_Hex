from PyQt5 import QtCore
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from hex_game.graphics.plot import StaticMplCanvas
from hex_game.graphics.debug import Debug
from hex_game.game import Game
from hex_game.graphics.hex_view import HexView
from PyQt5 import QtGui


class ResultsUI:
    def __init__(self, Ui_TIPE):
        self.Ui_TIPE = Ui_TIPE
        self.create_plots()
        self.widgetPlot = self.Ui_TIPE.widgetPlot
        self.dataframes = dict()
        self.Ui_TIPE.listWidgetResults.itemChanged.connect(self.update_results_list)

    def create_plots(self):
        self.Ui_TIPE.verticalLayoutResults.removeWidget(self.Ui_TIPE.widgetPlot)
        self.Ui_TIPE.verticalLayoutResults.removeWidget(self.Ui_TIPE.widgetToolbar)

        self.Ui_TIPE.widgetPlot.deleteLater()
        self.Ui_TIPE.widgetToolbar.deleteLater()

        self.Ui_TIPE.widgetPlot = StaticMplCanvas(self.Ui_TIPE.resultsTab, width=3, height=3, dpi=100)
        self.Ui_TIPE.widgetPlot.setObjectName("widgetPlot")
        self.Ui_TIPE.verticalLayoutResults.addWidget(self.Ui_TIPE.widgetPlot)

        self.Ui_TIPE.widgetToolbar = NavigationToolbar(self.Ui_TIPE.widgetPlot, self.Ui_TIPE.resultsTab)
        self.Ui_TIPE.widgetToolbar.setObjectName("widgetToolbar")
        self.Ui_TIPE.verticalLayoutResults.addWidget(self.Ui_TIPE.widgetToolbar)

    def add_result(self, result):
        name = result.split("/")[-1].split("\\")[-1]
        self.dataframes[name] = pd.read_hdf(result)

        self.widgetPlot.names.append(name)
        self.widgetPlot.enabled.append(True)
        self.widgetPlot.colors.append(np.random.rand(3,1))

        item = QListWidgetItem(name, self.Ui_TIPE.listWidgetResults)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)

    def update_results_list(self, item):
        if item.checkState():
            self.plot(self.dataframes[item.text()], self.Ui_TIPE.listWidgetResults.row(item))
        else:
            self.reload_plots()

    def reload_plots(self):
        self.widgetPlot.clear()
        for row in range(self.Ui_TIPE.listWidgetResults.count()):
            item = self.Ui_TIPE.listWidgetResults.item(row)
            if item.checkState():
                self.plot(self.dataframes[item.text()], row)

    def plot(self, df, row):
        epochs = df.epoch[len(df.epoch) - 1]
        color = self.widgetPlot.colors[row]
        self.widgetPlot.enabled[row] = True

        # Epsilon
        self.widgetPlot.epsilon.plot(df["epoch"], df["epsilon"], c=color)

        # Winner
        t = df[(df.winner != -1) & (df.epoch % 1000 < 100)][['epoch', 'winner', 'reward']]
        t = t.set_index(['epoch'])
        t['player 0'] = (t['winner'] == 0) & ((t['reward'] >= 0) | (t['reward'] == np.nan))
        t['player 1'] = (t['winner'] == 1) & ((t['reward'] >= 0) | (t['reward'] == np.nan))
        t['error'] = t['winner'] == 2
        t.drop('winner', 1, inplace=True)
        t.drop('reward', 1, inplace=True)
        k = int(epochs / 25000) * 1000
        t = t.groupby(pd.cut(t.index, np.arange(0, epochs + k, k))).sum()
        t.index = [i * k for i in range(len(t))]
        self.widgetPlot.winner.plot(t.index, t["player 0"] / (k / 1000), 'v-',
                                    t.index, t["player 1"] / (k / 1000), 'o-',
                                    t.index, t["error"] / (k / 1000), 'P-',
                                    c=color)

        # Loss
        self.widgetPlot.loss.plot(df["epoch"][df.loss.notnull() & df.random_move == False],
                                  df["loss"][df.loss.notnull() & df.random_move == False],
                                  'ro', alpha=0.1, markersize=0.1, c=color)

        # Draw
        self.widgetPlot.draw()
