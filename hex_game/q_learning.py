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
    """
    Init model with size size
    :param size: size
    :return: model
    """
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


def get_move_q_learning(board, player, model, training=False):
    """
    Get the move of a Q player
    :param board: board
    :param player: player
    :param model: model
    :param training: True if action and split_board are needed
    :return: (move, q_values, action, split_board) if training else (move, q_value)
    """
    size = board.shape[0]
    split_board = get_split_board(board, player)
    # Predict
    X = np.array([split_board])
    Y = model.predict(X, batch_size=1)
    # Get best move
    [q_values] = Y
    action = np.argmax(q_values)
    i = np.unravel_index(action, (size, size))
    move = (i[0], i[1]) if player == 0 else (i[1], i[0])
    if training:
        return move, q_values, action, split_board
    else:
        return move, q_values


def learn(size, gamma, start_epoch, end_epoch, random_epochs, initial_model_path="", reset_epsilon=False, thread=None,
          batch_size=1):
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
    :param batch_size: batch size
    :return: model, dataframe
    """

    ##################
    ### Load model ###
    ##################
    if initial_model_path == "":
        model = init_model(size)
    else:
        model = keras.models.load_model(initial_model_path)

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

    #####################
    ### Create memory ###
    #####################
    old_states_memory = np.zeros((batch_size, 3 * size ** 2))
    actions_memory = np.zeros(batch_size, dtype=int)
    new_states_memory = np.zeros((batch_size, 3 * size ** 2))
    rewards_memory = np.zeros(batch_size)
    terminals_memory = np.zeros(batch_size, dtype=bool)

    ###########################
    ### Initialize counters ###
    ###########################
    array_counter = 0
    last_array_counter = 0
    memory_counter = 0

    rewards = {"won": 1, "lost": -1, "error": -10, "nothing": 0}

    #######################
    ### Start main loop ###
    #######################
    epoch = start_epoch
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
                loss_log = loss_array[l:a][(epoch_array[l:a] % 1000 < 100) &
                                           (loss_array[l:a] != 0) &
                                           np.logical_not(np.isnan(loss_array[l:a]))].mean()
                w = winner_array[l:a][epoch_array[l:a] % 1000 < 100]
                c = (w != -1).sum()
                player0 = (w == 0).sum() / c * 100
                player1 = (w == 1).sum() / c * 100
                error = (w == 2).sum() / c * 100
                thread.log(epoch, loss_log, player0, player1, error)
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
        ai_random_state = np.random.RandomState(epoch)
        q_random_state = np.random.RandomState(epoch)

        #################################
        ### Initialize temp variables ###
        #################################
        actions = [None, None]
        split_boards = [None, None]

        #################
        ### Game loop ###
        #################
        while True:
            random_move = np.nan
            loss = np.nan

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
                    # Save action and splitboard
                    actions[current_player] = q_action
                    split_boards[current_player] = q_split_board
                    # Random move?
                    random_move = random.random() < epsilon and abs(epoch % 1000) > 100
                    # Get move
                    if random_move:
                        move = get_random_move(board, q_random_state)  # Limit regret
                    else:
                        move = q_move
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
                    action = actions[current_player]
                    old_state = split_boards[current_player]
                    reward = rewards["error"]
                    terminal = True
                else:
                    #
                    # Update other player
                    #
                    action = actions[other_player]
                    old_state = split_boards[other_player]
                    # Get update
                    if winner == current_player:
                        reward = rewards["lost"]
                        terminal = True
                    elif winner == other_player:
                        reward = rewards["won"]
                        terminal = True
                    else:  # winner == -1
                        reward = rewards["nothing"]
                        terminal = False
                        new_state = get_split_board(board, other_player)
                #
                # Save to memory
                #
                old_states_memory[memory_counter] = old_state
                actions_memory[memory_counter] = action
                if not terminal:
                    new_states_memory[memory_counter] = new_state
                rewards_memory[memory_counter] = reward
                terminals_memory[memory_counter] = terminal

            ########################
            ### Learn from memory ##
            ########################
            if memory_counter == batch_size - 1:
                X_train = old_states_memory
                Y_train = np.zeros((batch_size, size ** 2))

                for i in range(batch_size):
                    old_state = old_states_memory[i]
                    action = actions_memory[i]
                    new_state = new_states_memory[i]
                    reward = rewards_memory[i]
                    terminal = terminals_memory[i]

                    X = np.array([old_state])
                    Y = model.predict(X, batch_size=1)
                    [old_q_values] = Y

                    if terminal:
                        update = reward
                    else:
                        X = np.array([new_state])
                        Y = model.predict(X, batch_size=1)
                        [new_q_values] = Y
                        update = reward + gamma * max(new_q_values)

                    old_q_values[action] = update
                    Y_train[i] = old_q_values

                history = History()
                model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=1, verbose=0, callbacks=[history])
                loss = history.history["loss"][0]
                memory_counter = 0

            ###########
            ### Log ###
            ###########
            epoch_array[array_counter] = epoch
            winner_array[array_counter] = winner
            epsilon_array[array_counter] = epsilon
            random_move_array[array_counter] = random_move
            loss_array[array_counter] = loss
            move_count_array[array_counter] = move_count

            ########################
            ### Update counters ###
            ########################
            array_counter += 1
            move_count += 1
            memory_counter += 1

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
                           move_count=move_count_array[:array_counter]
                           ))
    ###########
    ### End ###
    ###########
    return model, df

# def learn_rules(model, size, epochs, batch_size):
#     for epoch in range(epochs):
#         X = np.zeros((batch_size, 3 * size ** 2))
#         Y = np.zeros((batch_size, size ** 2))
#         for i in range(batch_size):
#             board = np.random.randint(-1, 2, size=(size, size))
#             split_board = get_split_board(board, 0)
#             q_values = model.predict(split_board, batch_size=1)
#             q_values[0][board.flatten() != -1] = -10
#
#             X[i] = split_board[0]
#             Y[i] = q_values[0]
#         model.fit(X, Y, batch_size=batch_size, nb_epoch=1, verbose=0)
