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
        self.dataframes = dict()
        self.paths = []
        self.ui.listWidgetResults.itemChanged.connect(self.update_results_list)

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
        self.dataframes[name] = pd.read_hdf(path)

        self.paths.append(path)
        self.widgetPlot.names.append(name)
        self.widgetPlot.enabled.append(True)
        self.widgetPlot.colors.append(cm.get_cmap("Set1")(len(self.widgetPlot.colors)))

        item = QListWidgetItem(name, self.ui.listWidgetResults)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)

    def update_results_list(self, item: QListWidgetItem):
        """
        Update item state
        :param item: item of listWidgetResults
        :return:
        """
        if item.checkState():
            self.plot(self.dataframes[item.text()], self.ui.listWidgetResults.row(item))
        else:
            self.reload_plots()

    def reload_plots(self):
        """
        Clear plots and redraw
        """
        self.widgetPlot.clear()
        for row in range(self.ui.listWidgetResults.count()):
            item = self.ui.listWidgetResults.item(row)
            if item.checkState():
                self.plot(self.dataframes[item.text()], row)

    def plot(self, df: pd.DataFrame, row):
        """
        Plot a dataframe
        :param df: dataframe to plot
        :param row: row in listWidgetResults of the dataframe
        """
        color = self.widgetPlot.colors[row]
        self.widgetPlot.enabled[row] = True
        _, _, start_epoch, end_epoch, _, _, _ = hex_io.get_parameters(self.paths[row])

        # Epsilon
        self.widgetPlot.epsilon.plot(df["epoch"], df["epsilon"], c=color)

        # Winner
        k = int(round(end_epoch / 25000 + 0.5) * 1000)
        c_start = int(round(start_epoch / k))
        c_end = int(round(end_epoch / k))

        player0 = np.zeros(c_end - c_start)
        player1 = np.zeros(c_end - c_start)
        error = np.zeros(c_end - c_start)
        index = np.zeros(c_end - c_start)
        for i in range(c_start, c_end):
            index[i - c_start] = k * i
            m = (i * k < df.epoch) & (df.epoch < (i + 1) * k)
            w = df.winner[m][df.epoch[m] % 1000 < 100]
            x = (w != -1).sum()
            if x != 0:
                player0[i - c_start] = (w == 0).sum() / x * 100
                player1[i - c_start] = (w == 1).sum() / x * 100
                error[i - c_start] = (w == 2).sum() / x * 100

        self.widgetPlot.winner.plot(index, player0, 'v-',
                                    index, player1, 'o-',
                                    index, error, 'P-',
                                    c=color)

        # Loss
        self.widgetPlot.loss.plot(df["epoch"],
                                  df["loss"],
                                  'ro', alpha=1, markersize=1, c=color)

        # Draw
        self.widgetPlot.draw()
