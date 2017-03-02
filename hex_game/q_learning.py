import random
import warnings
from collections import deque

import numpy as np
import pandas as pd
import keras.models
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.optimizers import RMSprop
from hex_game.main import *
from hex_game.winner_check import *


def init_model(size):
    """
    Init model with size size
    :param size: size
    :return: model
    """
    model = Sequential()
    model.add(Convolution2D(32, 5, 5, init="lecun_uniform", input_shape=(size + 4, size + 4, 6,), border_mode="valid"))
    model.add(Activation('relu'))
    model.add(Convolution2D(32, 3, 3, init="lecun_uniform", border_mode="valid"))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(size ** 2, init="lecun_uniform"))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


def get_features(board, player):
    """
    Return the features corresponding to player
    :param board: board
    :param player: player
    :return: features
    """
    if player == 1:
        board = board.T
    size = board.shape[0]

    t = -numpy.ones((size + 4, size + 4, 6))

    t[2:-2, 2:-2, 0] = (board == player) * 2 - 1
    t[2:-2, 2:-2, 1] = (board == 1 - player) * 2 - 1

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


def get_action(model, split_board):
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


def get_move_from_action(player, action, size):
    i = np.unravel_index(action, (size, size))  # type: tuple
    move = (i[0], i[1]) if player == 0 else (i[1], i[0])
    return move


def get_move_q_learning(board, player, model):
    size = board.shape[0]
    split_board = get_features(board, player)
    action = get_action(model, split_board)
    move = get_move_from_action(player, action, size)
    return move


def get_random_action(board: np.ndarray, state: np.random.RandomState):
    board = board.flatten()
    actions = [k[0] for k in numpy.argwhere(board == -1)]
    state.shuffle(actions)
    return actions[0]


def learn(size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs, memory_size,
          q_players=(1,), allow_freeze=(0, 1), initial_models_path=("", ""), thread=None):
    """
    Train the model
    :return: model, dataframe
    """

    ##################
    ### Load model ###
    ##################
    models = [None, None]

    for player in range(2):
        if player in q_players:
            if initial_models_path[player] == "":
                models[player] = init_model(size)
            else:
                models[player] = keras.models.load_model(initial_models_path[player])

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
    array_counter = 0
    last_array_counter = 0

    ######################
    ### Set parameters ###
    ######################
    epsilon = initial_epsilon
    epoch = 0
    frozen_players = []

    #######################
    ### Start main loop ###
    #######################
    while True:
        epoch += 1

        ##################
        ### Thread Log ###
        ##################
        if epoch % 100 == 0:
            thread.set_epoch(epoch)
            if epoch % 1000 == 0:
                l = last_array_counter
                a = array_counter
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    loss_log_player0 = loss_array_player0[l:a][np.logical_not(np.isnan(loss_array_player0[l:a]))].mean()
                    loss_log_player1 = loss_array_player1[l:a][np.logical_not(np.isnan(loss_array_player1[l:a]))].mean()
                w = winner_array[l:a]
                c = (w != -1).sum()
                player0 = (w == 0).sum() / c * 100
                player1 = (w == 1).sum() / c * 100
                error = (w == 2).sum() / c * 100
                thread.log(epoch, loss_log_player0, loss_log_player1, player0, player1, error)
                last_array_counter = array_counter
                if player0 > 75 and 0 in allow_freeze:
                    frozen_players = [0]
                elif player1 > 75 and 1 in allow_freeze:
                    frozen_players = [1]
                else:
                    frozen_players = []

        #######################
        ### Break main loop ###
        #######################
        if epoch >= exploration_epochs + train_epochs or thread.stop:
            break

        ###################
        ### Set epsilon ###
        ###################
        if epsilon > final_epsilon:
            epsilon -= (initial_epsilon - final_epsilon) / exploration_epochs
        else:
            epsilon = 0

        ###############################################
        ### Create board and winner_check variables ###
        ###############################################
        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        winner = -1
        move_count = 0
        current_player = 0
        ai_random_state = np.random.RandomState()
        q_random_state = np.random.RandomState()

        #################################
        ### Initialize temp variables ###
        #################################
        actions = [None, None]
        states = [None, None]

        #################
        ### Game loop ###
        #################
        while True:
            x = 1 - move_count / size ** 2
            rewards = {"won": 5 * x, "lost": -5 * x, "error": -10, "nothing": 0}

            random_move = np.nan
            losses = [np.nan, np.nan]

            other_player = 1 - current_player
            current_player_is_q = current_player in q_players
            other_player_is_q = other_player in q_players
            current_player_is_learning = not current_player in frozen_players
            other_player_is_learning = not other_player in frozen_players

            ################################################
            ### If game already ended, just update model ###
            ################################################
            if winner == -1:
                ##################################
                ### Get move and save q values ###
                ##################################
                if current_player_is_q:
                    # Compute split board
                    split_board = get_features(board, current_player)

                    # Random move?
                    random_move = random.random() < epsilon

                    # Get action
                    if random_move:
                        action = get_random_action(board, q_random_state)  # Limit regret
                    else:
                        action = get_action(models[current_player], split_board)

                    # Save action and split board
                    actions[current_player] = action
                    states[current_player] = split_board

                    # Get move
                    move = get_move_from_action(current_player, action, size)
                else:
                    move = get_random_move(board, ai_random_state)

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
            if (other_player_is_q and other_player_is_learning and winner != 2 and move_count != 0) or \
                    (current_player_is_q and current_player_is_learning and winner == 2):
                if current_player_is_q and current_player_is_learning and winner == 2:
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
                        new_state = get_features(board, other_player)
                #
                # Save to memory
                #
                memory.append((old_state, action, new_state, reward, terminal))

            ########################
            ### Learn from memory ##
            ########################
            for player in range(2):
                model = models[player]
                memory = memories[player]
                if len(memory) == memory_size:
                    X = np.zeros((batch_size, size + 4, size + 4, 6))
                    Y = np.zeros((batch_size, size ** 2))

                    minibatch = random.sample(memory, batch_size)

                    for i in range(batch_size):
                        old_state, action, new_state, reward, terminal = minibatch[i]

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
                    memory.clear()

            ###########
            ### Log ###
            ###########
            epoch_array[array_counter] = epoch
            winner_array[array_counter] = winner
            epsilon_array[array_counter] = epsilon
            random_move_array[array_counter] = random_move
            loss_array_player0[array_counter] = losses[0]
            loss_array_player1[array_counter] = losses[1]
            move_count_array[array_counter] = move_count

            ########################
            ### Update counters ###
            ########################
            array_counter += 1
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

    ########################
    ### Create dataframe ###
    ########################
    df = pd.DataFrame(dict(epoch=epoch_array[:array_counter],
                           winner=winner_array[:array_counter],
                           epsilon=epsilon_array[:array_counter],
                           random_move=random_move_array[:array_counter],
                           loss_player0=loss_array_player0[:array_counter],
                           loss_player1=loss_array_player1[:array_counter],
                           move_count=move_count_array[:array_counter]
                           ))
    ###########
    ### End ###
    ###########
    return models, df
