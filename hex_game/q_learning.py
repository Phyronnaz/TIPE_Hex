import random
import warnings
import numpy as np
import pandas as pd
import keras.models
import tensorflow as tf

from hex_game.ai_poisson import get_move_poisson
from hex_game.main import *
from collections import deque
from keras.models import Sequential
from hex_game.winner_check import *
from keras.optimizers import RMSprop
from keras.initializers import Initializer
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D

rewards = {"won": 1, "lost": -1, "error": -1, "nothing": 0}


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
    model.add(Conv2D(filters=64, kernel_size=(5, 5), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform",
                     input_shape=(size + 4, size + 4, 6)))
    model.add(Activation('relu'))

    # model.add(Conv2D(filters=64, kernel_size=(5, 5), padding="same", data_format="channels_last", use_bias=True,
    #                  kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    # model.add(Activation('relu'))
    #
    # model.add(Conv2D(filters=64, kernel_size=(5, 5), padding="same", data_format="channels_last", use_bias=True,
    #                  kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    # model.add(Activation('relu'))

    # Neighbors 1 (3 layers)
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", data_format="channels_last", use_bias=True,
                     kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    # model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", data_format="channels_last", use_bias=True,
    #                  kernel_initializer="lecun_uniform" bias_initializer="lecun_uniform"))
    # model.add(Activation('relu'))
    #
    # model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", data_format="channels_last", use_bias=True,
    #                  kernel_initializer="lecun_uniform", bias_initializer="lecun_uniform"))
    # model.add(Activation('relu'))

    # Dense (1 layer)
    model.add(Flatten())
    model.add(Dense(size ** 2, kernel_initializer="lecun_uniform"))
    model.add(Activation('sigmoid'))

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

    # Borders set to 1 in all lines
    t[:2, :, 0] = 1
    t[-2:, :, 0] = 1
    t[:2, :, 2] = 1
    t[-2:, :, 3] = 1
    t[:, :2, 1] = 1
    t[:, -2:, 1] = 1
    t[:2, :, 4] = 1
    t[-2:, :, 5] = 1

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


def get_action(model: keras.models.Model, split_board: np.ndarray) -> int:
    """
    Get the move of a Q player
    :param model: model
    :param split_board: precomputed split board
    :return: q_values, action
    """
    # Predict
    [q_values] = model.predict(np.array([split_board]))

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


def train(model, size, n):
    X = np.empty((n, size + 4, size + 4, 6))
    Y = np.empty((n, size * size), dtype=int)

    for i in range(n):
        if i % 100 == 0:
            print(i)

        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        winner = -1
        current_player = 0
        while winner == -1:
            if current_player == 0:
                move = get_move_poisson(board, 0, debug_path=False)
                features = get_features(board)
                [q_values] = model.predict(numpy.array([features]))
                q_values[get_action_from_move(move, size)] = rewards["won"]
                q_values[board.flat != -1] = rewards["error"]

                X[i] = features
                Y[i] = q_values
            else:
                move = get_random_move(board)

            if can_play_move(board, move):
                board[move] = current_player
                winner, winner_counter = check_for_winner(move, current_player, winner_matrix, winner_counter)
            else:
                winner = 2

    for k in range(10 * n):
        if k % 100 == 0:
            print(k)
        l = random.sample(range(n), 64)
        model.train_on_batch(X[l], Y[l])


def learn(size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs, memory_size,
          q_players=(1,), models_path=("", ""), thread=None):
    """
    Train the model
    :return: model, dataframe
    """

    ##################
    ### Load model ###
    ##################
    models = [None, None]  # type: list[keras.models.Model]

    for player in range(2):
        if player in q_players:
            if models_path[player] == "":
                models[player] = init_model(size)
                train(models[player], size, 1000)
            else:
                models[player] = keras.models.load_model(models_path[player])

    #####################
    ### Create arrays ###
    #####################
    n = (exploration_epochs + train_epochs) * size ** 2
    epoch_array = np.zeros(n)
    winner_array = np.zeros(n)
    epsilon_array = np.zeros(n)
    random_move_array = np.zeros(n, dtype='bool')
    loss_array_player0 = np.zeros(n)
    loss_array_player1 = np.zeros(n)
    move_count_array = np.zeros(n)

    #######################
    ### Create memories ###
    #######################
    memories = [deque(), deque()]

    ###########################
    ### Initialize counters ###
    ###########################
    index = 0
    log_index = 0

    ######################
    ### Set parameters ###
    ######################
    epsilon = initial_epsilon
    epoch = 1  # avoid problems with %

    #######################
    ### Main loop ###
    #######################
    while epoch < exploration_epochs + train_epochs and not thread.stop:
        ##################
        ### Thread Log ###
        ##################
        if epoch % 1 == 0:
            thread.set_epoch(epoch)
            if epoch % 10 == 0:
                s = log_index
                e = index
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    loss_log_player0 = loss_array_player0[s:e][np.logical_not(np.isnan(loss_array_player0[s:e]))].mean()
                    loss_log_player1 = loss_array_player1[s:e][np.logical_not(np.isnan(loss_array_player1[s:e]))].mean()
                w = winner_array[s:e]
                c = (w != -1).sum()
                player0 = (w == 0).sum() / c * 100
                player1 = (w == 1).sum() / c * 100
                error = (w == 2).sum() / c * 100
                thread.log(epoch, loss_log_player0, loss_log_player1, player0, player1, error)
                log_index = index

        ###################
        ### Set epsilon ###
        ###################
        if epsilon > final_epsilon:
            epsilon -= (initial_epsilon - final_epsilon) / exploration_epochs
        else:
            epsilon = final_epsilon

        ###############################################
        ### Create board and winner_check variables ###
        ###############################################
        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        winner = -1  # -1: nothing, 0/1: winner, 2: error
        move_count = 0
        current_player = 0

        #################################
        ### Initialize temp variables ###
        #################################
        actions = [None, None]
        states = [None, None]

        #################
        ### Game loop ###
        #################
        while True:
            random_move = np.nan
            losses = [np.nan, np.nan]

            other_player = 1 - current_player

            #########################
            ### If game not ended ###
            #########################
            if winner == -1:
                ##################################
                ### Get move and save q values ###
                ##################################
                if current_player in q_players:
                    i_board = invert_board(board, current_player)
                    # Compute split board
                    split_board = get_features(i_board)

                    # Random move?
                    random_move = random.random() < epsilon

                    # Get action
                    if random_move:
                        action = get_random_action(i_board)  # Limit regret by not choosing completely random action
                    else:
                        action = get_action(models[current_player], split_board)

                    # Save action and split board
                    actions[current_player] = action
                    states[current_player] = split_board

                    # Get move
                    i_move = get_move_from_action(action, size)
                    move = invert_move(i_move, current_player)
                else:
                    move = get_random_move(board)

                ###################################
                ### Play move and update winner ###
                ###################################
                if can_play_move(board, move):
                    board[move] = current_player
                    winner, winner_counter = check_for_winner(move, current_player, winner_matrix, winner_counter)
                else:
                    winner = 2

            ######################
            ### Update players ###
            ######################
            if (other_player in q_players and winner != 2 and move_count != 0) or \
                    (current_player in q_players and winner == 2):
                if current_player in q_players and winner == 2:
                    #
                    # Error: Update current player and quit
                    #
                    memory = memories[current_player]
                    action = actions[current_player]
                    old_state = states[current_player]
                    reward = rewards["error"]
                    terminal = True
                    new_state = None
                else:
                    #
                    # Update other player
                    #
                    memory = memories[other_player]
                    action = actions[other_player]
                    old_state = states[other_player]
                    # Get update
                    if winner == current_player:
                        reward = rewards["lost"]
                        terminal = True
                        new_state = None
                    elif winner == other_player:
                        reward = rewards["won"]
                        terminal = True
                        new_state = None
                    else:  # winner == -1
                        reward = rewards["nothing"]
                        terminal = False
                        new_state = get_features(invert_board(board, other_player))
                #
                # Save to memory
                #
                if len(memory) == memory_size:
                    memory.popleft()
                memory.append((old_state, action, new_state, reward, terminal))

            ########################
            ### Learn from memory ##
            ########################
            for player in q_players:
                model = models[player]
                memory = memories[player]
                if len(memory) >= batch_size:  # enough experiences
                    X = np.zeros((batch_size, size + 4, size + 4, 6))
                    Y = np.zeros((batch_size, size ** 2))

                    batch = random.sample(memory, batch_size)

                    for i in range(batch_size):
                        old_state, action, new_state, reward, terminal = batch[i]

                        [old_q_values] = model.predict(np.array([old_state]))

                        if terminal:
                            update = reward
                        else:
                            [new_q_values] = model.predict(np.array([new_state]))
                            update = reward + gamma * max(new_q_values)

                        old_q_values[action] = update

                        X[i] = old_state
                        Y[i] = old_q_values

                    losses[player] = model.train_on_batch(X, Y)

            ###########
            ### Log ###
            ###########
            epoch_array[index] = epoch
            winner_array[index] = winner
            epsilon_array[index] = epsilon
            random_move_array[index] = random_move
            loss_array_player0[index] = losses[0]
            loss_array_player1[index] = losses[1]
            move_count_array[index] = move_count

            ########################
            ### Update counters ###
            ########################
            index += 1
            move_count += 1

            ######################
            ### Quit if needed ###
            ######################
            if winner == 2 or winner == other_player:
                break

            #####################
            ### Invert player ###
            #####################
            current_player = other_player

        #######################
        ### Increment epoch ###
        #######################
        epoch += 1

    ########################
    ### Create dataframe ###
    ########################
    df = pd.DataFrame(dict(epoch=epoch_array[:index],
                           winner=winner_array[:index],
                           epsilon=epsilon_array[:index],
                           random_move=random_move_array[:index],
                           loss_player0=loss_array_player0[:index],
                           loss_player1=loss_array_player1[:index],
                           move_count=move_count_array[:index]
                           ))
    ###########
    ### End ###
    ###########
    return models, df
