import threading
import datetime
import numpy as np
from hex_game import hex_io
from hex_game.q_learning import learn


class LearnThread(threading.Thread):
    def __init__(self, parameters, model):
        threading.Thread.__init__(self)

        self.n = parameters[6] + parameters[7]

        self.parameters = parameters
        self.model = model

        self.epoch_log = np.zeros(self.n)
        self.loss_log = np.zeros(self.n)
        self.player0_log = np.zeros(self.n)
        self.player1_log = np.zeros(self.n)
        self.error_log = np.zeros(self.n)
        self.index = 0

        self.start_time = datetime.datetime.now()
        self.elapsed_time = ""
        self.remaining_time = ""
        self.current_epoch = 0

        self.stop = False
        self.learning = False

    def run(self):
        self.stop = False
        self.learning = True
        hex_io.save_model_and_df(*learn(*self.parameters, initial_model_path=self.model, thread=self), *self.parameters)
        self.learning = False

    def get_progress(self):
        """
        Return progress of the learning
        :return: float between 0 and 1
        """
        return self.current_epoch / self.n

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
        total = int(elapsed * self.n / (epoch + 1))

        self.elapsed_time = datetime.timedelta(seconds=elapsed)
        self.remaining_time = datetime.timedelta(seconds=total - elapsed)
