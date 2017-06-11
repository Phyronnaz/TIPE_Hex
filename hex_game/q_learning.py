import os
import random
from collections import deque

import keras.models
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.initializers import Initializer
from keras.layers.convolutional import Conv2D
from keras.layers.core import Dense, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import RMSprop

from hex_game import hex_io
from hex_game.ai_poisson import get_move_poisson
from hex_game.main import *
from hex_game.winner_check import *


class Neighbors1(Initializer):
    def __call__(self, shape, dtype=None):
        x = np.random.random(shape)
        y = np.zeros(shape, dtype="float32")
        for (a, b) in NEIGHBORS_1:
            p = (a + 1, b + 1)
            y[p] = x[p]
        return tf.Variable(y)


class Neighbors2(Initializer):
    def __call__(self, shape, dtype=None):
        x = np.random.random(shape)
        y = np.zeros(shape, dtype="float32")
        for (a, b) in NEIGHBORS_2:
            p = (a + 2, b + 2)
            y[p] = x[p]
        return tf.Variable(y)


def init_model(size):
    """
    Init model with size size
    :param size: size
    :return: model
    """
    # http://deeplearning.net/software/theano/tutorial/conv_arithmetic.html
    #
    # filters: with 32: (x, y, z) -> (32, y, z)
    # kernel_size: (w, h)
    # strides: (d_w, d_h) distance between two consecutive positions of the kernel
    # padding: "valid": not applied on border / "same": applied on borders with added 0s
    # data_format: channels_last : inputs shape (batch, height, width, channels)
    #              channels_first: inputs shape (batch, channels, height, width)
    # dilation_rate: (d_w, d_h)
    # activation: If you don't specify anything, no activation is applied (ie. "linear" activation: a(x) = x).
    # use_bias: Boolean, whether the layer uses a bias vector.
    # kernel_initializer: Initializer for the kernel weights matrix.
    # bias_initializer: Initializer for the bias vector.
    # kernel_regularizer: Regularizer function applied to the kernel weights matrix.
    # bias_regularizer: Regularizer function applied to the bias vector.
    # activity_regularizer: Regularizer function applied to the output of the layer.
    # kernel_constraint: Constraint function applied to the kernel matrix.
    # bias_constraint: Constraint function applied to the bias vector.

    model = Sequential()

    # Neighbors 2 (3 layers)
    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform",
                     input_shape=(size + 4, size + 4, 6)))
    model.add(Activation('relu'))

    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    # Neighbors 1 (3 layers)
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    # Dense (1 layer)
    model.add(Flatten())
    model.add(Dense(size ** 2, kernel_initializer="lecun_uniform"))
    model.add(Activation('tanh'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


def get_features(board):
    """
    Return features of board
    :param board: board
    :return: features
    """
    size = board.shape[0]

    t = -numpy.ones((size + 4, size + 4, 6))

    # line 0: 1 if tile is owned by player 0, else -1
    # line 1: 1 if tile is owned by player 1, else -1
    # line 2: 1 if tile is owned by player 0 and connected to upper right border, else -1
    # line 3: 1 if tile is owned by player 0 and connected to lower left border, else -1
    # line 4: 1 if tile is owned by player 1 and connected to upper left border, else -1
    # line 5: 1 if tile is owned by player 1 and connected to lower right border, else -1

    t[2:-2, 2:-2, 0] = (board == 0) * 2 - 1
    t[2:-2, 2:-2, 1] = (board == 1) * 2 - 1

    # Borders
    t[:2, :, 0] = 1
    t[-2:, :, 0] = 1
    t[:2, :, 2] = 1
    t[-2:, :, 3] = 1
    t[:, :2, 1] = -1
    t[:, -2:, 1] = -1
    t[:2, :, 4] = -1
    t[-2:, :, 5] = -1

    t[:2, :2, :] = 0
    t[:2, -2:, :] = 0
    t[-2:, :2, :] = 0
    t[-2:, -2:, :] = 0

    # print(t[:, :, 0])

    # Paths
    for player in range(2):
        for side in range(2):
            checked = numpy.zeros(board.shape, dtype=bool)
            size = board.shape[0]
            pile = deque()

            # Append edges
            for a in range(size):
                if player == 0 and board[-side, a] == 0:
                    pile.append((0, a))
                elif player == 1 and board[a, -side] == 1:
                    pile.append((a, 0))

            # Process tiles
            while len(pile) != 0:
                x, y = pile.pop()

                if 0 <= x < size and 0 <= y < size and board[x, y] == player and not checked[x, y]:
                    checked[x, y] = True
                    pile.append((x - 1, y))
                    pile.append((x + 1, y))
                    pile.append((x, y - 1))
                    pile.append((x, y + 1))
                    pile.append((x + 1, y - 1))
                    pile.append((x - 1, y + 1))

            # Save
            t[2:-2, 2:-2, 2 + 2 * player + side] = checked * 2 - 1

    return t


def get_action(model: keras.models.Model, features: np.ndarray) -> int:
    """
    Get the move of a Q player
    :param model: model
    :param features: precomputed split board
    :return: q_values, action
    """
    # Predict
    [q_values] = model.predict(np.array([features]))

    # Get best action
    action = np.argmax(q_values)

    return action


def get_move_from_action(action: int, size: int) -> (int, int):
    return np.unravel_index(action, (size, size))


def get_action_from_move(move: (int, int), size: int) -> int:
    return np.ravel_multi_index(move, (size, size))


def get_move_q_learning(board: np.ndarray, player: int, model: keras.models.Model) -> (int, int):
    i_board = invert_board(board, player)
    size = i_board.shape[0]
    split_board = get_features(i_board)
    action = get_action(model, split_board)
    move = get_move_from_action(action, size)
    return invert_move(move, player)


def get_random_action(board: np.ndarray) -> int:
    return get_action_from_move(get_random_move(board), board.shape[0])


def create_database(size, n):
    boards = deque()
    actions = deque()
    for i in range(n):
        if i % 100 == 0:
            print("Creating database for size {}: {}% ({})".format(size, round(100 * i / n, 2), i))

        board = init_board(size)
        winner = -1

        while winner == -1:
            move = get_move_poisson(board, 0, debug_path=False)

            boards.append(board.copy())
            actions.append(get_action_from_move(move, size))

            if random.random() < 3 / 4:
                move = get_random_move(board)

            board[move] = 0

            if has_win(board, 0):
                winner = 0
            elif has_win(board, 1):
                winner = 1

            board = invert_board(board, 1)
    return np.array([boards, actions])


def train(model, database):
    X, Y = database

    n = len(X)
    size = X[0].shape[0]

    def f(a, b):
        l = np.zeros((len(b), size ** 2))
        for i in range(len(l)):
            l[i][b[i]] = 1
        return np.array([get_features(board) for board in a]), l

    m = 1000
    for i in range(m):
        print("Training: {}% ({})".format(round(100 * i / m, 2), i))
        l = random.sample(range(n), 64)
        model.train_on_batch(*f(X[l], Y[l]))


def get_norm(model, database):
    s = 0
    for i in range(10):
        board = database[0, int(len(database) * i / 10)]
        features = get_features(board)
        [q_values] = model.predict(numpy.array([features]))
        s += (q_values ** 2).mean()
    return s / 10


def learn(size, epochs, memory_size, batch_size, model_path="", thread=None, intermediate_save=False):
    """
    Train the model
    :return: model, dataframe
    """
    ##########################
    ## Create/Load database ##
    ##########################
    path = os.path.expanduser("~") + "/Hex/database_{}.npy".format(size)
    if os.path.exists(path):
        database = np.load(path)
    else:
        database = create_database(size, 10000)
        np.save(path, database)

    ##################
    ### Load model ###
    ##################
    if model_path == "":
        model = init_model(size)
        train(model, database)
    else:
        model = keras.models.load_model(model_path)

    #####################
    ### Create arrays ###
    #####################
    winner_array = np.zeros(epochs)
    loss_array = np.zeros(epochs)
    norm_array = np.zeros(epochs)

    thread.winner_array = winner_array
    thread.loss_array = loss_array

    #######################
    ### Create memories ###
    #######################
    memory = deque()

    ###########################
    ### Initialize counters ###
    ###########################
    index = 0

    ######################
    ### Set parameters ###
    ######################
    epsilon = 0.1
    epoch = 1  # avoid problems with %

    #######################
    ### Main loop ###
    #######################
    while epoch < epochs and not thread.stop:
        ##################
        ### Thread Log ###
        ##################
        thread.set_epoch(epoch)

        if epoch % 1000 == 0 and intermediate_save:
            print("Starting save")
            df = pd.DataFrame(dict(winner=winner_array[:index],
                                   loss=loss_array[:index],
                                   norm=norm_array[:index]
                                   ))
            hex_io.save_model_and_df(model, df, size, epochs, memory_size, batch_size, "current_epoch_{}".format(epoch))
            print("Save successful")
        #
        # if epoch == 100:
        #     import matplotlib.pyplot as plt
        #     plt.plot(range(index), loss_array[:index])
        #     plt.show()
        #
        #     plt.plot(range(index), norm_array[:index])
        #     plt.show()

        ########################
        ### Learn from memory ##
        ########################
        loss = np.nan
        if len(memory) >= batch_size:  # enough experiences
            X = np.zeros((batch_size, size + 4, size + 4, 6))
            Y = np.zeros((batch_size, size ** 2))

            batch = random.sample(memory, batch_size)

            old_states = np.array([b[0] for b in batch])
            new_states = np.array([b[2] for b in batch])

            old_q_values = model.predict(old_states)
            new_q_values = model.predict(new_states)

            for i in range(batch_size):
                _, action, _, reward, terminal = batch[i]

                if terminal:
                    update = reward
                else:
                    update = reward - max(new_q_values[i])

                old_q_values[i][action] = update

                X[i] = old_states[i]
                Y[i] = old_q_values[i]

            loss = model.train_on_batch(X, Y, )

        ###############################################
        ### Create board and winner_check variables ###
        ###############################################
        board = random.choice(database[0]).copy()
        winner = -1

        #################
        ### Game loop ###
        #################
        while winner == -1:
            ##################################
            ### Get move and save q values ###
            ##################################
            # Compute features
            features = get_features(board)

            # Random move?
            random_move = random.random() < epsilon

            # Get action
            if random_move:
                action = get_random_action(board)  # Limit regret by not choosing completely random action
            else:
                action = get_action(model, features)

            # Get move
            move = get_move_from_action(action, size)

            #################
            ### Play move ###
            #################
            if can_play_move(board, move):
                board[move] = 0
            else:
                winner = 2

            ##################
            ## Invert board ##
            ##################
            board = invert_board(board, 1)

            ################
            ## Flip board ##
            ################
            if random.random() > 0.5:
                board = flip(board)

            ####################
            ## Save to memory ##
            ####################
            if len(memory) == memory_size:
                memory.popleft()
            old_state = features
            new_state = get_features(board)

            if has_win(board, 1):
                winner = 1
                reward = 1
                terminal = True
            elif winner == 2:
                reward = -1
                terminal = True
            else:
                reward = 0
                terminal = False

            memory.append((old_state, action, new_state, reward, terminal))

        ###########
        ### Log ###
        ###########
        winner_array[index] = winner
        loss_array[index] = loss
        norm_array[index] = get_norm(model, database)

        ########################
        ### Update counters ###
        ########################
        index += 1

        #######################
        ### Increment epoch ###
        #######################
        epoch += 1

    ########################
    ### Create dataframe ###
    ########################
    df = pd.DataFrame(dict(winner=winner_array[:index],
                           loss=loss_array[:index],
                           norm=norm_array[:index]
                           ))
    ###########
    ### End ###
    ###########
    return model, df
