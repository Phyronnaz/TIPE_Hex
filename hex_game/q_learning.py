import random
import warnings
from collections import deque

import numpy as np
import pandas as pd
import keras.models
from keras.models import Sequential
from keras.layers.core import Dense, Activation
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
    model.add(Dense(size ** 2 * 4, init="lecun_uniform", input_shape=(3 * size ** 2,)))
    model.add(Activation('relu'))
    model.add(Dense(size ** 2 * 4, init="lecun_uniform"))
    model.add(Activation('relu'))
    model.add(Dense(size ** 2 * 4, init="lecun_uniform"))
    model.add(Activation('relu'))
    model.add(Dense(size ** 2, init="lecun_uniform"))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


def get_split_board(board, player):
    """
    Return the split board corresponding to player
    :param board: board
    :param player: player
    :return: split board
    """
    if player == 1:
        board = board.T
    size = board.shape[0]
    t = numpy.zeros((3, size, size))
    t[0] = (board == -1) * 2 - 1
    t[1] = (board == player) * 2 - 1
    t[2] = (board == 1 - player) * 2 - 1
    return t.flatten()


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
    split_board = get_split_board(board, player)
    action = get_action(model, split_board)
    move = get_move_from_action(player, action, size)
    return move


def get_random_action(board: np.ndarray, state: np.random.RandomState):
    board = board.flatten()
    actions = [k[0] for k in numpy.argwhere(board == -1)]
    state.shuffle(actions)
    return actions[0]


def learn(size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs, memory_size,
          q_players=(1,), initial_models_path=("", ""), thread=None):
    """
    Train the model=
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

    #####################
    ### Create memories ###
    #####################
    memories = [deque(), deque()]

    ###########################
    ### Initialize counters ###
    ###########################
    array_counter = 0
    last_array_counter = 0

    rewards = {"won": 1, "lost": -1, "error": -10, "nothing": 0}

    #######################
    ### Start main loop ###
    #######################
    epsilon = initial_epsilon
    epoch = 0
    while True:
        epoch += 1

        ##################
        ### Thread Log ###
        ##################
        if epoch % 100 == 0 and thread is not None:
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

        #######################
        ### Break main loop ###
        #######################
        if epoch >= exploration_epochs + train_epochs or (thread is not None and thread.stop):
            break

        ###################
        ### Set epsilon ###
        ###################
        if epsilon > final_epsilon:
            epsilon -= (initial_epsilon - final_epsilon) / exploration_epochs

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
            random_move = np.nan
            losses = [np.nan, np.nan]

            other_player = 1 - current_player
            current_player_is_q = current_player in q_players
            other_player_is_q = other_player in q_players

            ################################################
            ### If game already ended, just update model ###
            ################################################
            if winner == -1:
                ##################################
                ### Get move and save q values ###
                ##################################
                if current_player_is_q:
                    # Compute split board
                    split_board = get_split_board(board, current_player)

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
            if (other_player_is_q and winner != 2 and move_count != 0) or (current_player_is_q and winner == 2):
                if current_player_is_q and winner == 2:
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
                        new_state = get_split_board(board, other_player)
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
                    X = np.zeros((batch_size, 3 * size ** 2))
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
