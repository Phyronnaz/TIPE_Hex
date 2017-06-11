import os
import sys

# path = os.path.dirname(os.path.realpath(__file__))[:-8]
path = "/home/victor/PycharmProjects/TIPE_Hex/"
if path not in sys.path:
    sys.path.insert(0, path)

import numpy as np

from hex_game.q_learning import create_database

size = int(sys.argv[1])

path = os.path.expanduser("~") + "/Hex/database_{}.npy".format(size)
if os.path.exists(path):
    database = np.load(path)
else:
    database = create_database(size, 10000)
    np.save(path, database)