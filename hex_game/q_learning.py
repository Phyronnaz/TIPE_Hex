import random
import time
import datetime
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.callbacks import History
from keras.utils.visualize_util import plot
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


def learn(size=3, epochs=25000, gamma=0.8, first_player=True, early_reward=False, save_path="/notebooks/admin/saves",
          save=True):
    """
    Train the model
    :param size: size of the game
    :param epochs: number of games
    :param gamma: gamma for Q learning
    :param first_player: is AI beginning?
    :param early_reward: if no winner and no mistake, reward = move count
    :param save_path: path of the save folder
    :param save: save results?
    :return: model, dataframe
    """

    model = init_model(size)
    # plot(model, to_file='model.png')

    epsilon = 1

    index = np.arange(0, epochs * size ** 2)
    epoch_ser = pd.Series(index=index)
    winner_ser = pd.Series(index=index)
    epsilon_ser = pd.Series(index=index)
    random_move_ser = pd.Series(index=index, dtype='bool')
    loss_ser = pd.Series(index=index)
    reward_ser = pd.Series(index=index)
    move_count_ser = pd.Series(index=index)
    random_ai_move_ser = pd.Series(index=index, dtype='bool')

    ser_counter = 0

    start_time = time.time()

    print("Epochs : {}, gamma: {}, size : {}, early reward : {}, first player : {}".
          format(epochs, gamma, size, early_reward, first_player))

    for epoch in range(epochs):
        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        random_state = np.random.RandomState(epoch)
        winner = -1
        move_count = 0
        player = 0
        while winner == -1:
            if (first_player and player == 0) or (not first_player and player == 1):
                # Save board
                split_board = get_splitted_board(board, player)
                # Get move
                qval = model.predict(split_board, batch_size=1)
                random_move = random.random() < epsilon
                action = np.random.randint(0, size ** 2) if random_move else np.argmax(qval)
                move = action // size, action % size

                # Play move
                if can_play_move(board, move):
                    board[move] = player
                    winner, winner_counter = check_for_winner(move, player, winner_matrix, winner_counter)
                    move_count += 1
                else:
                    winner = 2

                # Observe reward
                if winner == -1:
                    reward = move_count if early_reward else 0
                elif winner == player:
                    reward = 2 * size ** 2
                elif winner == 1 - player:
                    reward = -2 * size ** 2
                elif winner == 2:
                    reward = -2 * size ** 2

                # Get max_Q(S',a)
                newQ = model.predict(get_splitted_board(board, player), batch_size=1)
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

                # Log
                epoch_ser[ser_counter] = epoch
                winner_ser[ser_counter] = winner
                epsilon_ser[ser_counter] = epsilon
                random_move_ser[ser_counter] = random_move
                loss_ser[ser_counter] = history.history["loss"][0]
                reward_ser[ser_counter] = reward
                move_count_ser[ser_counter] = move_count
                random_ai_move_ser[ser_counter] = False
                ser_counter += 1
            else:
                # AI
                move = get_move_random(board, random_state)
                board[move] = player
                winner, winner_counter = check_for_winner(move, player, winner_matrix, winner_counter)
                move_count += 1
                # Log
                epoch_ser[ser_counter] = epoch
                winner_ser[ser_counter] = winner
                move_count_ser[ser_counter] = move_count
                random_ai_move_ser[ser_counter] = True
                ser_counter += 1
            player = (1 - player) % 2
        # Log
        if epoch % 1000 == 0 and epoch != 0:
            t = round((epochs - epoch) * (time.time() - start_time) / epoch, 0)
            t_s = datetime.datetime.fromtimestamp(t).strftime('%M:%S')
            print("Game #: %s | Remaining time %s" % (epoch, t_s))

        epsilon -= 1 / epochs

    columns = (
        'size', 'gamma', 'first_player', 'early_reward', 'epoch', 'winner', 'epsilon', 'random_move', 'loss', 'reward',
        'move count')

    df = pd.DataFrame(dict(size=size,
                           gamma=gamma,
                           first_player=first_player,
                           early_reward=early_reward,
                           epoch=epoch_ser[:ser_counter],
                           winner=winner_ser[:ser_counter],
                           epsilon=epsilon_ser[:ser_counter],
                           random_move=random_move_ser[:ser_counter],
                           loss=loss_ser[:ser_counter],
                           reward=reward_ser[:ser_counter],
                           move_count=move_count_ser[:ser_counter],
                           random_ai_move=random_ai_move_ser[:ser_counter]
                           ))

    # Save
    if save:
        content = size, gamma, first_player, early_reward, epochs, datetime.datetime.now().isoformat()
        name = "size-{}-gamma-{}-first_player-{}-early_reward-{}-epochs-{}-date-{}".format(*content)
        model.save(save_path + "/models/" + name + ".model")
        df.to_hdf(save_path + "/stats/" + name + ".h5", 'df')

    return model, df
