import random
import datetime
import numpy as np
import pandas as pd
import keras.models
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
from keras.callbacks import History
from hex_game.main import *
from hex_game.winner_check import *


def init_model(size):
    model = Sequential()
    model.add(Dense(size ** 2 * 4, init='lecun_uniform', input_shape=(size ** 2 * 3,)))
    model.add(Activation('relu'))
    model.add(Dense(size ** 2 * 4, init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dense(size ** 2 * 4, init='lecun_uniform'))
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
    t[0] = (board == -1) * 2 - 1
    t[1] = (board == player) * 2 - 1
    t[2] = (board == 1 - player) * 2 - 1
    return t.reshape(1, 3 * size ** 2)


def get_move_q_learning(board, player, model, training=False):
    size = board.shape[0]
    split_board = get_split_board(board, player)
    # Predict
    q_values = model.predict(split_board, batch_size=1)
    # Get best move
    action = np.argmax(q_values)
    i = np.unravel_index(action, (size, size))
    move = (i[0], i[1]) if player == 0 else (i[1], i[0])
    if training:
        return move, q_values, action, split_board
    else:
        return move, q_values


def learn(size, gamma, start_epoch, end_epoch, random_epochs, initial_model_path="", reset_epsilon=False, thread=None):
    """
    Train the model
    :param size: size of the game
    :param gamma: gamma for Q learning
    :param start_epoch: start epoch
    :param end_epoch: end epoch
    :param random_epochs: number of epochs AI plays against random player
    :param initial_model_path: path of the model to start with
    :param reset_epsilon: reset epsilon ?
    :param thread: thread object
    :return: model, dataframe
    """

    ##################
    ### Load model ###
    ##################
    if initial_model_path == "":
        model = init_model(size)
    else:
        model = keras.models.load_model(initial_model_path)

    #######################
    ### Learn the rules ###
    #######################
    learn_rules(model, size, 10000)

    #####################
    ### Create arrays ###
    #####################
    n = (end_epoch - start_epoch) * size ** 2
    epoch_array = np.zeros(n)
    winner_array = np.zeros(n)
    epsilon_array = np.zeros(n)
    random_move_array = np.zeros(n, dtype='bool')
    loss_array = np.zeros(n)
    update_array = np.zeros(n)
    move_count_array = np.zeros(n)

    ###########################
    ### Initialize counters ###
    ###########################
    array_counter = 0
    last_array_counter = 0

    rewards = {"won": 1, "lost": -1, "error": -10, "nothing": 0}

    #######################
    ### Start main loop ###
    #######################
    epoch = start_epoch
    while True:
        epoch += 1
        #######################
        ### Learn the rules ###
        #######################
        learn_rules(model, size, 10)

        ##################
        ### Thread Log ###
        ##################
        if epoch % 100 == 0 and thread is not None:
            thread.set_epoch(epoch)
            if epoch % 1000 == 0:
                l = last_array_counter
                a = array_counter
                loss = loss_array[l:a][(epoch_array[l:a] % 1000 < 100) &
                                       (loss_array[l:a] != 0) &
                                       np.logical_not(np.isnan(loss_array[l:a]))].mean()
                w = winner_array[l:a][epoch_array[l:a] % 1000 < 100]
                c = (w != -1).sum()
                player0 = (w == 0).sum() / c * 100
                player1 = (w == 1).sum() / c * 100
                error = (w == 2).sum() / c * 100
                thread.log(epoch, loss, player0, player1, error)
                last_array_counter = array_counter

        #######################
        ### Break main loop ###
        #######################
        if epoch >= end_epoch or (thread is not None and thread.stop):
            break

        ###################
        ### Set epsilon ###
        ###################
        epsilon = (1000 / (epoch - start_epoch)) if reset_epsilon else (1000 / epoch)
        epsilon = min(1, epsilon)

        ###############################################
        ### Create board and winner_check variables ###
        ###############################################
        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        winner = -1
        move_count = 0
        player = 0
        random_state = np.random.RandomState(epoch)

        #################################
        ### Initialize temp variables ###
        #################################
        actions = [None, None]
        split_boards = [None, None]
        values = [None, None]

        #################
        ### Game loop ###
        #################
        while True:
            random_move = np.nan
            loss = np.nan
            update = np.nan

            current_player = player
            other_player = 1 - player
            current_player_is_q = epoch > random_epochs or player == 1
            other_player_is_q = epoch > random_epochs or player == 0

            ################################################
            ### If game already ended, just update model ###
            ################################################
            if winner == -1:
                ##################################
                ### Get move and save q values ###
                ##################################
                if current_player_is_q:
                    # Get q results
                    q_move, q_values, q_action, q_split_board = get_move_q_learning(board, current_player, model, True)
                    # Save action, splitboard and q_values
                    actions[current_player] = q_action
                    split_boards[current_player] = q_split_board
                    values[current_player] = q_values
                    # Random move?
                    random_move = random.random() < epsilon and abs(epoch % 1000) > 100
                    # Get move
                    if random_move:
                        move = tuple(np.random.randint(size, size=2))
                    else:
                        move = q_move
                else:
                    move = get_random_move(board, random_state)

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
                    action = actions[current_player]
                    q_values = values[current_player]
                    split_board = split_boards[current_player]
                    update = rewards["error"]
                else:
                    #
                    # Update other player
                    #
                    action = actions[other_player]
                    q_values = values[other_player]
                    split_board = split_boards[other_player]
                    # Get update
                    if winner == current_player:
                        update = rewards["lost"]
                    elif winner == other_player:
                        update = rewards["won"]
                    else:  # winner == -1
                        newQ = model.predict(get_split_board(board, other_player), batch_size=1)
                        maxQ = np.max(newQ)
                        update = rewards["nothing"] + gamma * maxQ
                #
                # Apply update
                #
                history = History()
                q_values[0][action] = update
                model.fit(split_board, q_values, batch_size=1, nb_epoch=1, verbose=0, callbacks=[history])
                loss = history.history["loss"][0]

            ###########
            ### Log ###
            ###########
            epoch_array[array_counter] = epoch
            winner_array[array_counter] = winner
            epsilon_array[array_counter] = epsilon
            random_move_array[array_counter] = random_move
            loss_array[array_counter] = loss
            update_array[array_counter] = update
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
            player = 1 - player

    ########################
    ### Create dataframe ###
    ########################
    df = pd.DataFrame(dict(epoch=epoch_array[:array_counter],
                           winner=winner_array[:array_counter],
                           epsilon=epsilon_array[:array_counter],
                           random_move=random_move_array[:array_counter],
                           loss=loss_array[:array_counter],
                           update=update_array[:array_counter],
                           move_count=move_count_array[:array_counter]
                           ))
    ###########
    ### End ###
    ###########
    return model, df


def learn_rules(model, size, epochs):
    for _ in range(epochs):
        board = np.random.randint(-1, 2, size=(size, size))
        split_board = get_split_board(board, 0)
        q_values = model.predict(split_board, batch_size=1)
        q_values[0][board.flatten() != -1] = -10
        model.fit(split_board, q_values, batch_size=1, nb_epoch=1, verbose=0)
