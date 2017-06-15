import matplotlib.pyplot as plt
import pandas as pd
import easygui
import os
import sys

# path = os.path.dirname(os.path.realpath(__file__))[:-8]
path = "/home/victor/PycharmProjects/TIPE_Hex/"
if path not in sys.path:
    sys.path.insert(0, path)


path = easygui.fileopenbox(default="/home/victor/Hex/")

df = pd.read_hdf(path)

n = len(df.loss)
d = 10000
y = n // d
x = [i * y for i in range(d)]


def f(l):
    return [l[k * y:(k + 1) * y].mean() for k in range(d)]


# plt.subplot(211)
# plt.subplot(212)

plt.plot(range(len(df.loss)), df.loss)
plt.xlabel("époque")
plt.ylabel("perte")
plt.show()

plt.plot(range(len(df.norm)), df.norm)
plt.xlabel("époque")
plt.ylabel("norme")
plt.show()
