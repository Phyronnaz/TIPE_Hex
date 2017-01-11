from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from game_handler import GameHandler
from hex_game import *
from tools import *
import random
import numpy
from player import Player

size = 5


def init_model(size: int):
    model = Sequential()
    model.add(Dense(64, init='lecun_uniform', input_shape=(size ** 2,)))
    model.add(Activation('relu'))
    # model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

    model.add(Dense(64, init='lecun_uniform'))
    model.add(Activation('relu'))
    # model.add(Dropout(0.2))

    model.add(Dense(size ** 2, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


model = init_model()

epochs = 100000
gamma = 0.9  # since it may take several moves to goal, making gamma high
epsilon = 1


def check_for_winner(move: Move, player: int, winner_matrix: numpy.ndarray, winner_counter: int) -> (int, int):
    winner = 0
    p = 2 * player - 1
    all_neighbors = [winner_matrix[n[0] + move[0], n[1] + move[1]] for n in NEIGHBORS_1]
    player_neighbors = numpy.array(list(set([k for k in all_neighbors if k * p > 0])))

    if len(player_neighbors) == 0:
        winner_matrix[move] = winner_counter * p
        winner_counter += 1
    elif len(player_neighbors) == 1:
        winner_matrix[move] = player_neighbors[0]
    elif 1 * p in player_neighbors and 2 * p in player_neighbors:
        winner = player
    else:
        m = min(abs(player_neighbors)) * p
        for k in player_neighbors:
            if k != m:
                winner_matrix[winner_matrix == k] = m
        winner_matrix[move] = m
    return winner, winner_counter


def init_winner_matrix_and_counter():
    winner_matrix = numpy.zeros(board.shape)
    winner_matrix[0, :] = -1
    winner_matrix[-1, :] = -2
    winner_matrix[:, 0] = 1
    winner_matrix[:, -1] = 2
    return winner_matrix, 3


def get_random_move(board: numpy.ndarray, random_state: numpy.random.RandomState):
    moves = get_possibles_moves(board)
    random_state.shuffle(moves)
    move = None
    for m in moves:
        if can_play_move(board, m):
            move = m
            break
    if move is None:
        raise Exception("move is None")
    else:
        return move


def get_q_action(qval: numpy.ndarray):
    if random.random() < epsilon / 10:  # choose random action
        action = numpy.random.randint(0, 4)
    else:  # choose best action from Q(s,a) values
        action = numpy.argmax(qval)
    return action


for i in range(epochs):
    board = init_board(visual_size=size - 2)
    winner_matrix, winner_counter = init_winner_matrix_and_counter()
    random_state = numpy.random.RandomState(0)
    winner = -1

    while winner == -1:
        # AI
        move = get_random_move(board, random_state)
        play_move(board, move, 0)
        winner, winner_counter = check_for_winner(move, 0, winner_matrix, winner_counter)

        # We are in state S
        # Let's run our Q function on S to get Q values for all possible actions
        qval = model.predict(board.reshape(1, size ** 2), batch_size=1)
        action = get_q_action(qval)
        move = action // size + 1, action % size + 1

        # Take action, observe new state S'
        play_move(board, move, 1)
        # Check for winner
        winner, winner_counter = check_for_winner(move, 1, winner_matrix, winner_counter)
        # Observe reward
        reward = 10 if winner == 1 else (-10 if winner == 0 else 0)
        # Get max_Q(S',a)
        newQ = model.predict(board.reshape(1, size ** 2), batch_size=1)
        maxQ = numpy.max(newQ)
        y = numpy.zeros((1, size ** 2))
        y[:] = qval[:]

        if reward == 0:
            update = reward + gamma * maxQ
        else:
            update = reward

        y[0][action] = update  # target output
        model.fit(board.reshape(1, size ** 2), y, batch_size=1, nb_epoch=1, verbose=0)

    if i % 10 == 0:
        print("Game #: %s Winner: %s" % (i, winner))
    if epsilon > 0.1:
        epsilon -= 1 / epochs

random_state = numpy.random.RandomState(0)
GameHandler(visual_size=size - 2, player0=Player(random_state))
