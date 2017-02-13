import threading
import numpy as np
from hex_game.q_learning import learn


class LearnThread(threading.Thread):
    def __init__(self, size, gamma, start_epoch, end_epoch, random_epochs, initial_model_path):
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

        self.elapsed_time = ""
        self.remaining_time = ""

        self.stop = False
        self.learning = False

        self.model = None
        self.df = None

    def run(self):
        self.learning = True
        self.model, self.df = learn(self.size, self.gamma, self.start_epoch, self.end_epoch, self.random_epochs,
                                    self.initial_model_path, self)
        self.learning = False

    def get_progress(self):
        return (self.epoch_log[self.index - 1] - self.start_epoch) / (self.end_epoch - self.start_epoch)

    def log(self, epoch, loss, player0, player1, error):
        self.epoch_log[self.index] = epoch
        self.loss_log[self.index] = loss
        self.player0_log[self.index] = player0
        self.player1_log[self.index] = player1
        self.error_log[self.index] = error
        self.index += 1

    def set_time(self, elapsed, remaining):
        self.elapsed_time = elapsed
        self.remaining_time = remaining
