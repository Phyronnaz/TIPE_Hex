import sys
import os
import numpy
from bokeh.plotting import output_file, show, figure, gridplot
from bokeh.palettes import Category10


def chooser():
    if len(sys.argv) < 2:
        print("Usage: graphs.py folder1 folder2 ...")
        return
    paths = []
    for a in sys.argv[1:]:
        if os.path.isdir(a):
            paths.append(a)
        else:
            print("{} is not a valid directory".format(a))

    print("Name?")
    name = input()
    f = figure(title=name, x_axis_label='epochs', y_axis_label='loss', webgl=True,
               tools="pan,wheel_zoom,box_zoom,reset,resize,save,crosshair")

    files = []
    for p in paths:
        files += [(p + k, k) for k in os.listdir(p) if k[-4:len(k)] == ".npy"]
    c = 0
    for p, n in files:
        l = n.split("-")
        loss = numpy.loadtxt(p, delimiter=" ")
        f.circle(loss[:, 0], loss[:, 1], legend="gamma=" + str(l[l.index("gamma") + 1]), alpha=0.2,
                 color=Category10[10][c] if c < 10 else "yellow", line_color=None)
        c += 1
    print("Output file?")
    of = input()
    output_file(of)
    show(f)


if __name__ == "__main__":
    chooser()
