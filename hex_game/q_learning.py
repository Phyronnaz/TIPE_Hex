import numpy
import random
import time
import datetime
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.callbacks import History
from keras.utils.visualize_util import plot
from bokeh.plotting import output_file, show, figure, gridplot
from hex_game.players import *
from hex_game.main import *
from hex_game.winner_check import *
from hex_game.utils import *
from hex_game.game import *


def init_model(size):
    model = Sequential()
    model.add(Dense(size ** 2, init='lecun_uniform', input_shape=(size * size * 3,)))
    # model.add(Activation('relu'))
    # model.add(Dense(size ** 2, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


def learn(size=3, epochs=25000, gamma=0.8, player=0, early_reward=False):
    batch_size = 1
    history = History()

    model = init_model(size)
    # plot(model, to_file='model.png')


    epsilon = 1

    move_count_array = numpy.zeros(epochs)
    winner_array = numpy.zeros(epochs)
    loss = numpy.zeros((epochs * size ** 2, 2))
    loss_c = 0

    start_time = time.time()

    print("Epochs : {}, Batch size: {}, gamma: {}, size : {}, early reward : {}, player : {}".
          format(epochs, batch_size, gamma, size, early_reward, player))

    for i in range(epochs):
        for j in range(batch_size):
            board = init_board(size)
            winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
            random_state = numpy.random.RandomState(i)
            winner = -1
            move_count = 0
            while winner == -1:
                if player == move_count % 2:
                    # Save board
                    splitted_board = get_splitted_board(board, player)
                    # Get move
                    qval = model.predict(splitted_board, batch_size=batch_size)
                    random_move = random.random() < epsilon
                    if random_move:
                        action = numpy.random.randint(0, size ** 2)
                    else:
                        action = numpy.argmax(qval)
                    move = action // size, action % size

                    # Play move
                    if can_play_move(board, move):
                        board[move] = player
                        winner, winner_counter = check_for_winner(move, player, winner_matrix, winner_counter)
                        move_count += 1
                    else:
                        winner = 3

                    # Observe reward
                    if winner == -1:
                        reward = move_count if early_reward else 0
                    elif winner == player:
                        reward = 2 * size ** 2
                    elif winner == 1 - player:
                        reward = -2 * size ** 2
                    elif winner == 3:
                        reward = -2 * size ** 2

                    # Get max_Q(S',a)
                    newQ = model.predict(get_splitted_board(board, player), batch_size=batch_size)
                    maxQ = numpy.max(newQ)

                    # Get update
                    if winner == -1:
                        update = reward + gamma * maxQ
                    else:
                        update = reward

                    qval[0][action] = update
                    model.fit(splitted_board, qval, batch_size=1, nb_epoch=1, verbose=0, callbacks=[history])
                    # Log
                    if not random_move:
                        loss[loss_c, 0] = i + move_count / size ** 2
                        loss[loss_c, 1] = history.history["loss"][0]
                        loss_c += 1
                else:
                    # AI
                    move = get_move_random(board, random_state)
                    board[move] = 1 - player
                    winner, winner_counter = check_for_winner(move, 1 - player, winner_matrix, winner_counter)
                    move_count += 1
            move_count_array[i] = move_count
            winner_array[i] = winner

            # Log
            if i % 1000 == 0 and i != 0:
                w_a = winner_array[max(i - 1000, 0): i]
                m_a = move_count_array[max(i - 1000, 0): i]
                l_a = loss[max(loss_c - 1000, 0): loss_c, 1]
                w = round(w_a.mean(), 2)
                m = round(m_a.mean(), 2)
                l = round(l_a.mean(), 2)

                deltatime = time.time() - start_time

                t = round((epochs - i) * deltatime / i, 0)
                t_s = datetime.datetime.fromtimestamp(t).strftime('%M:%S')

                print("Game #: %s | Average Winner %s | Average Move count %s | Average loss %s | Remaining time %s" % (
                    i, w, m, l, t_s))

        epsilon -= 1 / epochs

    # Graphs
    # x = [k for k in range(epochs)]
    #
    # f = figure(title="loss")
    # f.circle(loss[:loss_c, 0], loss[:loss_c, 1], alpha=0.1, line_color=None)

    # p2 = figure(title="winner")
    # p2.circle(x, winner_array, alpha=0.1, line_color=None)
    #
    # p3 = figure(title="move count")
    # p3.circle(x, move_count_array, alpha=0.1, line_color=None)

    return model, loss[:loss_c]
