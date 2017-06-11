import os
import sys

path = os.path.dirname(os.path.realpath(__file__))[:-8]
if path not in sys.path:
    sys.path.insert(0, path)

from PyQt5 import QtWidgets
from hex_game.graphics.ui import UI
from hex_game.threads.learn_thread import LearnThread

if len(sys.argv) > 1:
    for i in range(10):
        LearnThread(size=6, epochs=100000, memory_size=10000, batch_size=512, intermediate_save=False).run()
else:
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())