import os
import sys

import numpy as np

from hex_game.q_learning import create_database

path = os.path.dirname(os.path.realpath(__file__))[:-8]
if path not in sys.path:
    sys.path.insert(0, path)

from PyQt5 import QtWidgets
from hex_game.graphics import UI
from hex_game.threads.learn_thread import LearnThread

if len(sys.argv) > 1:
    LearnThread(size=5, epochs=100000, memory_size=10000, batch_size=512).run()
else:
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())



# size = 9
# path = os.path.expanduser("~") + "/Hex/database_{}.npy".format(size)
# if os.path.exists(path):
#     database = np.load(path)
# else:
#     database = create_database(size, 10000)
#     np.save(path, database)