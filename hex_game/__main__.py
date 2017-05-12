from getopt import getopt
import sys
import os

path = os.path.dirname(os.path.realpath(__file__))[:-8]
if path not in sys.path:
    sys.path.insert(0, path)

from PyQt5 import QtWidgets
from hex_game.graphics import UI

app = QtWidgets.QApplication(sys.argv)
ui = UI()
sys.exit(app.exec_())
