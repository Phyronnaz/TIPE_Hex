import threading
import datetime
import numpy as np
from hex_game import hex_io
from hex_game.q_learning import learn


class LearnThread(threading.Thread):
    def __init__(self, size, gamma, start_epoch, end_epoch, random_epochs, initial_model_path, reset_epsilon,
                 batch_size, part):
        threading.Thread.__init__(self)

        self.epoch_log = np.zeros(end_epoch - start_epoch)
        self.loss_log = np.zeros(end_epoch - start_epoch)
        self.player0_log = np.zeros(end_epoch - start_epoch)
        self.player1_log = np.zeros(end_epoch - start_epoch)
        self.error_log = np.zeros(end_epoch - start_epoch)
        self.index = 0

        self.size = size
        self.gamma = gamma
        self.start_epoch = start_epoch
        self.end_epoch = end_epoch
        self.random_epochs = random_epochs
        self.initial_model_path = initial_model_path
        self.reset_epsilon = reset_epsilon
        self.batch_size = batch_size
        self.part = part

        self.start_time = datetime.datetime.now()
        self.elapsed_time = ""
        self.remaining_time = ""
        self.current_epoch = 0

        self.stop = False
        self.learning = False

        self.model = None
        self.df = None

    def save(self):
        hex_io.save_model_and_df(self.model, self.df, self.size, self.gamma, self.start_epoch, self.end_epoch,
                                 self.random_epochs, self.batch_size, self.part)

    def run(self):
        self.stop = False
        self.learning = True
        self.model, self.df = learn(self.size, self.gamma, self.start_epoch, self.end_epoch, self.random_epochs,
                                    self.initial_model_path, self.reset_epsilon, self, self.batch_size)
        self.learning = False

    def get_progress(self):
        """
        Return progress of the learning
        :return: float between 0 and 1
        """
        return (self.current_epoch - self.start_epoch) / (self.end_epoch - self.start_epoch)

    def log(self, epoch, loss, player0, player1, error):
        """
        Add a row to the logs
        :param epoch: epoch
        :param loss: loss
        :param player0: percentage of game player 0 won
        :param player1: percentage of game player 1 won
        :param error: percentage of game ended with an error
        """
        self.epoch_log[self.index] = epoch
        self.loss_log[self.index] = loss
        self.player0_log[self.index] = player0
        self.player1_log[self.index] = player1
        self.error_log[self.index] = error
        self.index += 1

    def set_epoch(self, epoch):
        """
        Set epoch of the training
        :param epoch: epoch
        """
        self.current_epoch = epoch

        elapsed = int((datetime.datetime.now() - self.start_time).seconds)
        total = int(elapsed * (self.end_epoch - self.start_epoch) / (epoch - self.start_epoch + 1))

        self.elapsed_time = datetime.timedelta(seconds=elapsed)
        self.remaining_time = datetime.timedelta(seconds=total - elapsed)
