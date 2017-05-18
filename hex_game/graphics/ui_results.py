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
        self.widgetPlot.get_name = self.get_name

        self.dataframes = []
        self.paths = []
        self.cache = dict()
        self.ui.pushButtonRefresh.pressed.connect(self.reload_plots)
        self.ui.pushButtonClear.pressed.connect(self.clear)
        self.create_combox_box()

    def create_plot_and_toolbar(self):
        """
        Create the plot and toolbar widgets
        """
        self.ui.verticalLayoutResults.removeWidget(self.ui.widgetResultsPlot)
        self.ui.verticalLayoutResults.removeWidget(self.ui.widgetResultsToolbar)

        self.ui.widgetResultsPlot.deleteLater()
        self.ui.widgetResultsToolbar.deleteLater()

        self.ui.widgetResultsPlot = ResultsPlot(self.ui.resultsTab, width=5, height=5)
        self.ui.widgetResultsPlot.setObjectName("widgetResultsPlot")
        self.ui.verticalLayoutResults.addWidget(self.ui.widgetResultsPlot)

        self.ui.widgetResultsToolbar = NavigationToolbar(self.ui.widgetResultsPlot, self.ui.resultsTab)
        self.ui.widgetResultsToolbar.setObjectName("widgetResultsToolbar")
        self.ui.verticalLayoutResults.addWidget(self.ui.widgetResultsToolbar)

    def get_name(self, path):
        s = self.ui.comboBoxColorVariable.currentText()
        d = {"size": "Size", "epochs": "Epochs", "memory_size": "Memory size", "batch_size": "Batch size"}
        return d[s] + " = " + str(hex_io.get_parameters_dict(path)[s])

    def create_combox_box(self):
        for s in ["size", "epochs", "memory_size", "batch_size"]:
            self.ui.comboBoxColorVariable.addItem(s)
        l = list(cm.cmap_d.keys())
        l.sort()
        for s in l:
            self.ui.comboBoxColorMaps.addItem(s)

    def add_result(self, path):
        """
        Add a result
        :param path: path of the file
        :return:
        """
        name = hex_io.get_pretty_name(*hex_io.get_parameters(path))

        self.dataframes.append(pd.read_hdf(path))
        self.paths.append(path)

        self.widgetPlot.paths.append(path)
        self.widgetPlot.plot_enabled.append(True)

        self.widgetPlot.colors.append("black")

        item = QListWidgetItem(name, self.ui.listWidgetResults)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)

    def clear(self):
        for df in self.dataframes:
            del df
        self.ui.listWidgetResults.clear()
        self.dataframes = []
        self.paths = []
        self.cache = dict()
        self.widgetPlot.paths = []
        self.widgetPlot.plot_enabled = []
        self.widgetPlot.colors = []
        self.widgetPlot.clear()
        self.widgetPlot.draw()

    def reload_plots(self, *args):
        """
        Clear plots and redraw
        """
        for row in range(self.ui.listWidgetResults.count()):
            item = self.ui.listWidgetResults.item(row)
            checked = item.checkState() != 0
            self.widgetPlot.plot_enabled[row] = checked

            x = hex_io.get_parameters_dict(self.paths[row])[self.ui.comboBoxColorVariable.currentText()]
            x /= self.ui.doubleSpinBoxMaxPlot.value()
            self.widgetPlot.colors[row] = cm.get_cmap(self.ui.comboBoxColorMaps.currentText())(x)

        self.widgetPlot.clear()

        for row in range(self.ui.listWidgetResults.count()):
            item = self.ui.listWidgetResults.item(row)
            checked = item.checkState() != 0
            if checked:
                self.plot(row)
        self.widgetPlot.draw()

    def plot(self, row):
        """
        Plot a dataframe
        :param row: row in listWidgetResults of the dataframe
        """
        color = self.widgetPlot.colors[row]

        # Winner
        index, player, error, loss = self.get_arrays(row)

        self.widgetPlot.winner.plot(index, player, 'o-',
                                    index, error, 'P-',
                                    c=color, markersize=5)
        self.widgetPlot.winner.set_ybound(0, 100)
        self.widgetPlot.winner.set_xbound(0, max(index))

        # Loss
        self.widgetPlot.loss.plot(index, loss, 'o-', c=color, markersize=5)
        self.widgetPlot.loss.set_ybound(0, max(loss))
        self.widgetPlot.loss.set_xbound(0, max(index))

    def get_arrays(self, row):
        if row not in self.cache:
            df = self.dataframes[row]

            n = hex_io.get_parameters_dict(self.paths[row])["epochs"]

            k = n // 25

            player = np.zeros(25)
            error = np.zeros(25)
            loss = np.zeros(25)
            index = np.zeros(25)

            for i in range(25):
                index[i] = k * i
                loss[i] = df.loss[k * i:k * (i + 1)].mean()

                w = df.winner[k * i:(k * (i + 1))]
                player[i] = (w == 1).sum() / k * 100
                error[i] = (w == 2).sum() / k * 100
            self.cache[row] = index, player, error, loss
        return self.cache[row]
