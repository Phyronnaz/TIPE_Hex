import sys
import os

path = os.path.dirname(os.path.realpath(__file__))[:-8]
if path not in sys.path:
    sys.path.insert(0, path)

from PyQt5 import QtWidgets
from hex_game.graphics import UI
from hex_game.q_learning import learn


# learn(size=5, epochs=250000, gamma=0.9, save_path="/notebooks/admin/saves/Random_02-04-250000-size_5-random_250000",
#       save=True, load_model_path="", initial_epoch=0, initial_epsilon=1, random_epochs=250000)


app = QtWidgets.QApplication(sys.argv)
ui = UI(3)
sys.exit(app.exec_())
