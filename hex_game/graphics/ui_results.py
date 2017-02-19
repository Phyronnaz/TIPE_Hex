import numpy as np
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidgetItem
from matplotlib import cm
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from hex_game import hex_io
from hex_game.graphics.mainwindow import Ui_TIPE
from hex_game.graphics.plots import ResultsPlot


class ResultsUI:
    def __init__(self, ui: Ui_TIPE):
        self.ui = ui
        self.create_plot_and_toolbar()
        self.widgetPlot = self.ui.widgetResultsPlot  # type: ResultsPlot
        self.dataframes = []
        self.paths = []
        self.cache = dict()
        self.ui.listWidgetResults.itemChanged.connect(self.reload_plots)

    def create_plot_and_toolbar(self):
        """
        Create the plot and toolbar widgets
        """
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

    def add_result(self, path):
        """
        Add a result
        :param path: path of the file
        :return:
        """
        name = hex_io.get_pretty_name(*hex_io.get_parameters(path))

        self.dataframes.append(pd.read_hdf(path))
        self.paths.append(path)

        self.widgetPlot.names.append(name)
        self.widgetPlot.plot_enabled.append(True)
        self.widgetPlot.colors.append(cm.get_cmap("Set1")(len(self.widgetPlot.colors)))

        item = QListWidgetItem(name, self.ui.listWidgetResults)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)

    def reload_plots(self):
        """
        Clear plots and redraw
        """
        for row in range(self.ui.listWidgetResults.count()):
            item = self.ui.listWidgetResults.item(row)
            checked = item.checkState() != 0
            self.widgetPlot.plot_enabled[row] = checked

        self.widgetPlot.clear()

        for row in range(self.ui.listWidgetResults.count()):
            item = self.ui.listWidgetResults.item(row)
            checked = item.checkState() != 0
            if checked:
                self.plot(row)

    def plot(self, row):
        """
        Plot a dataframe
        :param df: dataframe to plot
        :param row: row in listWidgetResults of the dataframe
        """
        color = self.widgetPlot.colors[row]
        df = self.dataframes[row]

        # Epsilon
        self.widgetPlot.epsilon.plot(df["epoch"], df["epsilon"], c=color)

        # Winner

        index, player0, player1, error, loss = self.get_arrays(row)

        self.widgetPlot.winner.plot(index, player0, 'v-',
                                    index, player1, 'o-',
                                    index, error, 'P-',
                                    c=color, markersize=5)

        # Loss
        # self.widgetPlot.loss.plot(df["epoch"], df["loss"], 'ro', markersize=1, c=color)
        self.widgetPlot.loss.plot(index, loss, c=color)

        # Draw
        self.widgetPlot.draw()

    def get_arrays(self, row):
        if row not in self.cache:
            df = self.dataframes[row]
            _, _, _, _, _, _, exploration_epochs, train_epochs, _ = hex_io.get_parameters(self.paths[row])
            n = exploration_epochs + train_epochs
            k = int(round(n / 25000 + 0.5) * 1000)
            c_start = 0
            c_end = int(round(n / k))

            player0 = np.zeros(c_end - c_start)
            player1 = np.zeros(c_end - c_start)
            error = np.zeros(c_end - c_start)
            loss = np.zeros(c_end - c_start)
            index = np.zeros(c_end - c_start)
            for i in range(c_start, c_end):
                index[i - c_start] = k * i
                m = (i * k < df.epoch) & (df.epoch < (i + 1) * k)
                loss[i] = df.loss[m].mean()
                w = df.winner[m]
                x = (w != -1).sum()
                if x != 0:
                    player0[i - c_start] = (w == 0).sum() / x * 100
                    player1[i - c_start] = (w == 1).sum() / x * 100
                    error[i - c_start] = (w == 2).sum() / x * 100
            self.cache[row] = index, player0, player1, error, loss
        return self.cache[row]
