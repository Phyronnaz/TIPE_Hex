import random
import os
import time
import datetime
import numpy as np
import pandas as pd
# import keras.models
# from keras.models import Sequential
# from keras.layers.core import Dense, Dropout, Activation
# from keras.optimizers import RMSprop
# from keras.callbacks import History
# from keras.utils.visualize_util import plot
from hex_game.main import *
from hex_game.winner_check import *


def init_model(size):
    model = Sequential()
    model.add(Dense(size ** 2 * 4, init='lecun_uniform', input_shape=(size ** 2 * 3,)))
    model.add(Activation('relu'))
    model.add(Dense(size ** 2, init='lecun_uniform'))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


def print_time(epochs, epoch, start_time):
    t = round((epochs - epoch) * (time.time() - start_time) / epoch, 0)
    t_s = datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S')
    print("Game #: %s | Remaining time %s" % (epoch, t_s))


def get_split_board(board, player):
    if player == 1:
        board = board.T
    size = board.shape[0]
    t = numpy.zeros((3, size, size))
    t[0] = board == 0
    t[1] = board == 1 + player
    t[2] = board == 2 - player
    return t.reshape(1, size ** 2 * 3)


def get_move_q_learning(board, player, model, size, random_move=False):
    split_board = get_split_board(board, player)
    qval = model.predict(split_board, batch_size=1)
    action = np.random.randint(0, size ** 2) if random_move else np.argmax(qval)
    move = (action // size, action % size) if player == 0 else (action % size, action // size)
    return move, split_board, qval, action


def learn(size=3, epochs=25000, gamma=0.8, save_path="/notebooks/admin/saves", save=True, load_model_path="",
          initial_epoch=0, initial_epsilon=1, random_epochs=0):
    """
    Train the model
    :param size: size of the game
    :param epochs: number of games
    :param gamma: gamma for Q learning
    :param first_player: is AI beginning?
    :param save_path: path of the save folder
    :param save: save results?
    :param load_model_path: "" if no model to begin with
    :param initial_epoch: initial epoch
    :param initial_epsilon: initial epsilon
    :return: model, dataframe
    """
    if load_model_path == "":
        model = init_model(size)
    else:
        model = keras.models.load_model(load_model_path)

    epsilon = initial_epsilon

    n = epochs * size ** 2
    epoch_array = np.zeros(n)
    winner_array = np.zeros(n)
    epsilon_array = np.zeros(n)
    random_move_array = np.zeros(n, dtype='bool')
    loss_array = np.zeros(n)
    reward_array = np.zeros(n)
    move_count_array = np.zeros(n)

    array_counter = 0

    start_time = time.time()

    print("{} epochs, gamma={}, size={}".format(epochs, gamma, size))
    print("Start time: " + datetime.datetime.fromtimestamp(start_time).strftime('%D %H:%M:%S'))

    for epoch in range(initial_epoch, initial_epoch + epochs):
        # Print time left
        if epoch % 1000 == 0 and epoch != initial_epoch:
            print_time(epochs, epoch - initial_epoch, start_time)

        # Epsilon
        epsilon -= initial_epsilon / epochs

        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        winner = -1
        move_count = 0
        player = 0
        random_state = np.random.RandomState(epoch)
        while winner != 2 and winner != player:
            if random_epochs < epoch or player == 1:
                # Get move
                random_move = random.random() < epsilon and abs(epoch % 1000) > 100
                move, split_board, qval, action = get_move_q_learning(board, player, model, size, random_move)

                if winner == -1:
                    # Play move
                    if can_play_move(board, move):
                        board[move] = player
                        winner, winner_counter = check_for_winner(move, player, winner_matrix, winner_counter)
                    else:
                        winner = 2

                # Observe reward
                if winner == -1:
                    reward = 0
                elif winner == player:
                    reward = 2 * size ** 2
                elif winner == 1 - player:
                    reward = -2 * size ** 2
                elif winner == 2:
                    reward = -2 * size ** 2

                # Get max_Q(S',a)
                newQ = model.predict(get_split_board(board, player), batch_size=1)
                maxQ = np.max(newQ)

                # Get update
                if winner == -1:
                    update = reward + gamma * maxQ
                else:
                    update = reward

                # Fit the model
                qval[0][action] = update
                history = History()
                model.fit(split_board, qval, batch_size=1, nb_epoch=1, verbose=0, callbacks=[history])

                loss = history.history["loss"][0]
            else:
                # Random
                if winner == -1:
                    move = get_random_move(board, random_state)
                    board[move] = player
                    winner, winner_counter = check_for_winner(move, player, winner_matrix, winner_counter)

                random_move = np.nan
                loss = np.nan
                reward = np.nan

            # Log
            epoch_array[array_counter] = epoch
            winner_array[array_counter] = winner
            epsilon_array[array_counter] = epsilon
            random_move_array[array_counter] = random_move
            loss_array[array_counter] = loss
            reward_array[array_counter] = reward
            move_count_array[array_counter] = move_count

            array_counter += 1
            move_count += 1
            player = 1 - player

    # Dataframe
    df = pd.DataFrame(dict(size=size,
                           gamma=gamma,
                           epoch=epoch_array[:array_counter],
                           winner=winner_array[:array_counter],
                           epsilon=epsilon_array[:array_counter],
                           random_move=random_move_array[:array_counter],
                           loss=loss_array[:array_counter],
                           reward=reward_array[:array_counter],
                           move_count=move_count_array[:array_counter]
                           ))

    # Save
    if save:
        for directory in [save_path + "/models", save_path + "/stats"]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        content = size, gamma, epochs, datetime.datetime.now().isoformat()
        name = "size-{}-gamma-{}-epochs-{}-date-{}".format(*content)
        model.save(save_path + "/models/" + name + ".model")
        df.to_hdf(save_path + "/stats/" + name + ".h5", 'df', complevel=9, complib='blosc')

    return model, df
