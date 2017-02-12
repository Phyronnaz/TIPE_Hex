import random

import matplotlib
import matplotlib.lines as mlines
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class StaticMplCanvas(FigureCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.loss = self.fig.add_subplot(221)
        self.winner = self.fig.add_subplot(222)
        self.epsilon = self.fig.add_subplot(223)
        self.legend = self.fig.legend([], [], 'lower right')
        self.fig.set_tight_layout(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.names = []
        self.enabled = []
        self.colors = []
        self.name_plots()

    def name_plots(self):
        # Epsilon
        self.epsilon.set_title("Epsilon")
        self.epsilon.set_xlabel("epoch")
        self.epsilon.set_ylabel("epsilon")

        # Loss
        self.loss.set_title("Loss")
        self.loss.set_xlabel("epoch")
        self.loss.set_ylabel("loss")

        # Winner
        self.winner.set_title("Winner")
        self.winner.set_xlabel("epoch")
        self.winner.set_ylabel("percentage")

        labels = ["Player 0", "Player 1", "error"]
        markers = ["v", "o", "P"]
        colors = ["black", "black", "black"]
        lines = []
        for i in range(len(colors)):
            lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
        self.winner.legend(handles=lines)

        # Legend
        lines = []
        for i in range(len(self.names)):
            if self.enabled[i]:
                lines.append(mlines.Line2D([], [], color=self.colors[i], label=self.names[i], marker="o"))
        self.legend.remove()
        self.legend = self.fig.legend(lines, self.names, 'lower right')

        self.draw()

    def clear(self):
        self.epsilon.cla()
        self.loss.cla()
        self.winner.cla()
        self.name_plots()

# class DynamicMplCanvas(MplCanvas):
#     """A canvas that updates itself every second with a new plot."""
#
#     def __init__(self, *args, **kwargs):
#         MplCanvas.__init__(self, *args, **kwargs)
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(self.update_figure)
#         timer.start(1000)
#
#         self.compute_initial_figure()
#
#     def compute_initial_figure(self):
#         self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
#
#     def update_figure(self):
#         # Build a list of 4 random integers between 0 and 10 (both inclusive)
#         l = [random.randint(0, 10) for i in range(4)]
#         self.axes.cla()
#         self.axes.plot([0, 1, 2, 3], l, 'r')
#         self.draw()
