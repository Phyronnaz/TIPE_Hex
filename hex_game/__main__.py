from .q_learning import learn
from hex_game.game import Game
from hex_game.players import *
from bokeh.plotting import output_file, show, figure, gridplot
from bokeh.palettes import Category10
import numpy

epochs = 250000

path = "/home/admin/saves/2017-01-20/"

for size in [5]:
    figs = [0, 1]
    for early_reward in [False]:
        loss_array = []
        l = [0.01, 0.5, 1]
        for gamma in l:
            model, loss = learn(size=size, epochs=epochs, gamma=gamma, player=0, early_reward=early_reward)
            loss_array.append(loss)

            name = "size-{}_gamma-{}_player-{}_early_reward-{}".format(size, gamma, 0, early_reward)

            model.save(path + name + ".model")
            numpy.savetxt(path + name + ".npy", loss)

        name = "size={}, early reward={}".format(size, early_reward)
        f = figure(title=name, x_axis_label='epochs', y_axis_label='loss', webgl=True,
                   tools="pan,wheel_zoom,box_zoom,reset,resize,save,crosshair")

        for i in range(len(l)):
            f.circle(loss_array[i][:, 0], loss_array[i][:, 1], legend="gamma=" + str(l[i]), alpha=0.2,
                     color=Category10[10][i], line_color=None)

        figs[int(early_reward)] = f

    output_file(path + "output_" + str(size) + ".html")

    f = gridplot([figs])
    show(f)

# a = RandomPlayer()
# b = QPlayer(model)
# player0, player1 = (a, b) if player == 1 else (b, a)
# game = Game(size=size, player0=player0, player1=player1)
# game.start()
