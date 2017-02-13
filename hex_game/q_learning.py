import random
import datetime
import numpy as np
import pandas as pd
import keras.models
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
from keras.callbacks import History
from keras.utils.visualize_util import plot
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


def get_split_board(board, player):
    if player == 1:
        board = board.T
    size = board.shape[0]
    t = numpy.zeros((3, size, size))
    t[0] = board == 0
    t[1] = board == 1 + player
    t[2] = board == 2 - player
    return t.reshape(1, size ** 2 * 3)


def get_move_q_learning(board, player, model):
    size = board.shape[0]
    split_board = get_split_board(board, player)
    q_values = model.predict(split_board, batch_size=1)
    action = np.argmax(q_values)
    move = (action // size, action % size) if player == 0 else (action % size, action // size)
    return move, q_values


def learn(size, gamma, start_epoch, end_epoch, random_epochs, initial_model_path="", thread=None):
    """
    Train the model
    :param size: size of the game
    :param epochs: number of games
    :param gamma: gamma for Q learning
    :param start_epoch: start epoch
    :param end_epoch: end epoch
    :param initial_model_path: path of the model to start with
    :param random_epochs: number of epochs AI plays against random player
    :param thread: thread object
    :return: model, dataframe
    """

    if initial_model_path == "":
        model = init_model(size)
    else:
        model = keras.models.load_model(initial_model_path)

    epsilon = 1

    n = (end_epoch - start_epoch) * size ** 2
    epoch_array = np.zeros(n)
    winner_array = np.zeros(n)
    epsilon_array = np.zeros(n)
    random_move_array = np.zeros(n, dtype='bool')
    loss_array = np.zeros(n)
    reward_array = np.zeros(n)
    move_count_array = np.zeros(n)

    array_counter = 0

    last_array_counter = 0

    start_time = datetime.datetime.now()

    for epoch in range(start_epoch, end_epoch + 1):
        # Log
        if epoch % 100 == 0 and epoch != start_epoch:
            elapsed = int((datetime.datetime.now() - start_time).seconds)
            total = int(elapsed * (end_epoch - start_epoch) / (epoch - start_epoch))
            elapsed_time = datetime.timedelta(seconds=elapsed)
            remaining_time = datetime.timedelta(seconds=total - elapsed)
            # print("Game #: %s | Remaining time %s | Elapsed time %s" % (epoch, remaining_time, elapsed_time))

            if thread is not None and epoch % 1000 == 0:
                l = last_array_counter
                a = array_counter
                loss = loss_array[l:a][(epoch_array[l:a] % 1000 < 100) & \
                                       (loss_array[l:a] != 0) & \
                                       np.logical_not(np.isnan(loss_array[l:a]))].mean()
                w = winner_array[l:a][epoch_array[l:a] % 1000 < 100]
                c = (w != -1).sum()
                player0 = (w == 0).sum() / c * 100
                player1 = (w == 1).sum() / c * 100
                error = (w == 2).sum() / c * 100
                thread.log(epoch, loss, player0, player1, error)
                thread.set_time(elapsed_time, remaining_time)
                last_array_counter = array_counter

        # Break
        if epoch >= end_epoch or (thread is not None and thread.stop):
            break

        # Epsilon
        epsilon = max(0.1, epsilon - 1 / end_epoch)

        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        winner = -1
        move_count = 0
        player = 0
        random_state = np.random.RandomState(epoch)
        while winner != 2 and winner != player:
            if random_epochs < epoch or player == 1:
                # Save board
                split_board = get_split_board(board, player)
                # Get move
                random_move = random.random() < epsilon and abs(epoch % 1000) > 100

                q_values = model.predict(split_board, batch_size=1)
                action = np.random.randint(0, size ** 2) if random_move else np.argmax(q_values)
                move = (action // size, action % size) if player == 0 else (action % size, action // size)

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
                q_values[0][action] = update
                history = History()
                model.fit(split_board, q_values, batch_size=1, nb_epoch=1, verbose=0, callbacks=[history])

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
    df = pd.DataFrame(dict(epoch=epoch_array[:array_counter],
                           winner=winner_array[:array_counter],
                           epsilon=epsilon_array[:array_counter],
                           random_move=random_move_array[:array_counter],
                           loss=loss_array[:array_counter],
                           reward=reward_array[:array_counter],
                           move_count=move_count_array[:array_counter]
                           ))

    return model, df
