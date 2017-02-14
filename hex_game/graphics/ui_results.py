import numpy as np
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidgetItem
from matplotlib import cm
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from hex_game.graphics.mainwindow import Ui_TIPE
from hex_game.graphics.plots import ResultsPlot


class ResultsUI:
    def __init__(self, ui: Ui_TIPE):
        self.ui = ui
        self.create_plots()
        self.widgetPlot = self.ui.widgetResultsPlot
        self.dataframes = dict()
        self.ui.listWidgetResults.itemChanged.connect(self.update_results_list)

    def create_plots(self):
        self.ui.verticalLayoutResults.removeWidget(self.ui.widgetResultsPlot)
        self.ui.verticalLayoutResults.removeWidget(self.ui.widgetResultsToolbar)

        self.ui.widgetResultsPlot.deleteLater()
        self.ui.widgetResultsToolbar.deleteLater()

        self.ui.widgetResultsPlot = ResultsPlot(self.ui.resultsTab, width=3, height=3, dpi=100)
        self.ui.widgetResultsPlot.setObjectName("widgetResultsPlot")
        self.ui.verticalLayoutResults.addWidget(self.ui.widgetResultsPlot)

        self.ui.widgetResultsToolbar = NavigationToolbar(self.ui.widgetResultsPlot, self.ui.resultsTab)
        self.ui.widgetResultsToolbar.setObjectName("widgetResultsToolbar")
        self.ui.verticalLayoutResults.addWidget(self.ui.widgetResultsToolbar)

    def add_result(self, result):
        name = result.split("/")[-1].split("\\")[-1]
        self.dataframes[name] = pd.read_hdf(result)

        self.widgetPlot.names.append(name)
        self.widgetPlot.enabled.append(True)
        self.widgetPlot.colors.append(cm.get_cmap("Set1")(len(self.widgetPlot.colors)))

        item = QListWidgetItem(name, self.ui.listWidgetResults)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)

    def update_results_list(self, item):
        if item.checkState():
            self.plot(self.dataframes[item.text()], self.ui.listWidgetResults.row(item))
        else:
            self.reload_plots()

    def reload_plots(self):
        self.widgetPlot.clear()
        for row in range(self.ui.listWidgetResults.count()):
            item = self.ui.listWidgetResults.item(row)
            if item.checkState():
                self.plot(self.dataframes[item.text()], row)

    def plot(self, df, row):
        epochs = df.epoch.max()
        color = self.widgetPlot.colors[row]
        self.widgetPlot.enabled[row] = True

        # Epsilon
        self.widgetPlot.epsilon.plot(df["epoch"], df["epsilon"], c=color)

        # Winner
        k = int(round(epochs / 25000 + 0.5) * 1000)
        c = int(round(epochs / k))
        print(c)
        player0 = np.zeros(c)
        player1 = np.zeros(c)
        error = np.zeros(c)
        index = np.zeros(c)
        for i in range(c):
            index[i] = k * i
            m = (i * k < df.epoch) & (df.epoch < (i + 1) * k)
            w = df.winner[m][df.epoch[m] % 1000 < 100]
            x = (w != -1).sum()
            if x != 0:
                player0[i] = (w == 0).sum() / x * 100
                player1[i] = (w == 1).sum() / x * 100
                error[i] = (w == 2).sum() / x * 100

        self.widgetPlot.winner.plot(index, player0, 'v-',
                                    index, player1, 'o-',
                                    index, error, 'P-',
                                    c=color)

        # Loss
        self.widgetPlot.loss.plot(df["epoch"][df.loss.notnull() & df.random_move == False],
                                  df["loss"][df.loss.notnull() & df.random_move == False],
                                  'ro', alpha=1, markersize=1, c=color)

        # Draw
        self.widgetPlot.draw()
