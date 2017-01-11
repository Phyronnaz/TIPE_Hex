from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from hex_game import play_move, get_move_random, can_play_move, init_board
from winner_check import init_winner_matrix_and_counter, check_for_winner
from game import Game
from players.random import RandomPlayer
from players.q_ai import QPlayer
import random
import numpy


# TODO: graphs

def init_model(s: int):
    model = Sequential()
    model.add(Dense(2 * s ** 2, init='lecun_uniform', input_shape=(s ** 2,)))
    model.add(Activation('relu'))
    # model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

    model.add(Dense(2 * s ** 2, init='lecun_uniform'))
    model.add(Activation('relu'))
    # model.add(Dropout(0.2))

    model.add(Dense(s ** 2, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


size = 3
epochs = 10000
gamma = 0.1  # since it may take several moves to goal, making gamma high
epsilon = 1
player = 0  # AI begin

model = init_model(size)

for i in range(epochs):
    board = init_board(size)
    winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
    random_state = numpy.random.RandomState(0)
    winner = -1
    k = 0
    while winner == -1:
        if player == k % 2:
            # We are in state S
            # Let's run our Q function on S to get Q values for all possible actions
            qval = model.predict(board.reshape(1, size ** 2) * 2 - 1, batch_size=1)
            if random.random() < epsilon:  # choose random action
                action = numpy.random.randint(0, size ** 2)
            else:  # choose best action from Q(s,a) values
                action = numpy.argmax(qval)

            move = action // size, action % size

            # Get reward
            if can_play_move(board, move):
                # Take action, observe new state S'
                play_move(board, move, player)
                # Check for winner
                winner, winner_counter = check_for_winner(move, player, winner_matrix, winner_counter)
                k += 1
            else:
                winner = 3

            # Observe reward
            if winner == -1:
                reward = min(k, size)
            elif winner == player:
                reward = 2 * size ** 2
            elif winner == 1 - player:
                reward = -2 * size ** 2
            else:
                winner = -1
                reward = -1000

            # Get max_Q(S',a)
            newQ = model.predict(board.reshape(1, size ** 2), batch_size=1)
            maxQ = numpy.max(newQ)
            y = numpy.zeros((1, size ** 2))
            y[:] = qval[:]

            if winner == -1:
                update = reward + gamma * maxQ
            else:
                update = reward

            y[0][action] = update  # target output
            model.fit(board.reshape(1, size ** 2), y, batch_size=1, nb_epoch=1, verbose=0)
        else:
            # AI
            move = get_move_random(board, random_state)
            play_move(board, move, 1 - player)
            winner, winner_counter = check_for_winner(move, 1 - player, winner_matrix, winner_counter)
            k += 1

    if i % 10 == 0:
        print("Game #: %s Winner: %s Move count: %s" % (i, winner, k))

    epsilon -= 1 / epochs

random_state = numpy.random.RandomState(0)
a = RandomPlayer(random_state)
b = QPlayer(model)
player0, player1 = (a, b) if player == 1 else (b, a)
game = Game(size=size, player0=player0, player1=player1)
game.start()
