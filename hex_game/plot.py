import matplotlib.pyplot as plt
import pandas as pd
import easygui

path = easygui.fileopenbox(default="/home/victor/Hex/")

df = pd.read_hdf(path)

n = len(df.loss)
y = n // 25
x = [i * y for i in range(25)]


def f(l):
    return [l[k * y:(k + 1) * y].mean() for k in range(25)]


plt.subplot(211)
plt.plot(x, f(df.loss))
plt.subplot(212)
plt.plot(range(len(df.norm)), df.norm)

plt.show()
