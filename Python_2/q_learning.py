from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.callbacks import History
from hex_game import play_move, get_move_random, can_play_move, init_board
from winner_check import init_winner_matrix_and_counter, check_for_winner
from game import Game
from players import RandomPlayer
from players import QPlayer
from bokeh.plotting import output_file, show, figure
import random
import numpy


def init_model(size):
    model = Sequential()
    model.add(Dense(3 * size ** 2, init='lecun_uniform', input_shape=(size * size * 3,)))
    # model.add(Activation('relu'))
    # model.add(Dense(size ** 2, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    return model


def get_splitted_board(board):
    size = board.shape[0]
    t = numpy.zeros((3, size, size))
    t[0] = board == 0
    t[1] = board == 1
    t[2] = board == 2
    return t.reshape(1, size ** 2 * 3)


size = 5
epochs = 10000
batch_size = 1
gamma = 0.8  # since it may take several moves to goal, making gamma high
epsilon = 1
player = 0  # AI begin
history = History()

model = init_model(size)

nombre_coup = numpy.zeros(epochs)
winner_array = numpy.zeros(epochs)
loss = numpy.zeros(epochs)

print("Epochs : {}, Batch size: {}, gamma: {}, size : {}".format(epochs, batch_size, gamma, size))

for i in range(epochs):
    for j in range(batch_size):
        board = init_board(size)
        winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
        random_state = numpy.random.RandomState(0)
        winner = -1
        move_count = 0
        while winner == -1:
            if player == move_count % 2:
                # Save board
                old_board = numpy.copy(board)
                # Get move
                qval = model.predict(get_splitted_board(board), batch_size=batch_size)
                random_move = random.random() < epsilon
                if random_move:
                    action = numpy.random.randint(0, size ** 2)
                else:
                    action = numpy.argmax(qval)
                move = action // size, action % size

                # Play move
                if can_play_move(board, move):
                    play_move(board, move, player)
                    winner, winner_counter = check_for_winner(move, player, winner_matrix, winner_counter)
                    move_count += 1
                else:
                    winner = 3

                # Observe reward
                if winner == -1:
                    reward = move_count
                elif winner == player:
                    reward = 2 * size ** 2
                elif winner == 1 - player:
                    reward = -2 * size ** 2
                elif winner == 3:
                    reward = -2 * size ** 2

                # Get max_Q(S',a)
                newQ = model.predict(get_splitted_board(board), batch_size=batch_size)
                maxQ = numpy.max(newQ)

                # Get update
                if winner == -1:
                    update = reward + gamma * maxQ
                else:
                    update = reward

                qval[0][action] = update
                model.fit(get_splitted_board(old_board), qval, batch_size=1, nb_epoch=1, verbose=0, callbacks=[history])
                loss[i] = history.history["loss"][0] if not random_move else 0
            else:
                # AI
                move = get_move_random(board, random_state)
                play_move(board, move, 1 - player)
                winner, winner_counter = check_for_winner(move, 1 - player, winner_matrix, winner_counter)
                move_count += 1
        nombre_coup[i] = move_count
        winner_array[i] = winner

        if i % 10 == 0:
            print("Game #: %s Winner: %s Move count: %s" % (i, winner, move_count))

    epsilon -= 1 / epochs

# x = [k for k in range(epochs)]
# plt.plot(x, nombre_coup)
# plt.plot(x, winner_array)
# plt.show()


f = figure()
y = loss
f.circle([k for k in range(len(y))], y)
output_file("loss.html")
show(f)

random_state = numpy.random.RandomState(0)
a = RandomPlayer(random_state)
b = QPlayer(model)
player0, player1 = (a, b) if player == 1 else (b, a)
game = Game(size=size, player0=player0, player1=player1)
game.start()
