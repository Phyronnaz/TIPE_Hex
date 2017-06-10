import threading
import datetime
import numpy as np
from hex_game import hex_io
from hex_game.q_learning import learn

from hex_game.tf_init import sess


class LearnThread(threading.Thread):
    def __init__(self, size, epochs, memory_size, batch_size, comment="", model=""):
        threading.Thread.__init__(self)

        self.size = size
        self.epochs = epochs
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.comment = comment
        self.model = model

        self.winner_array = np.zeros(self.epochs)
        self.loss_array = np.zeros(self.epochs)

        self.start_time = -1
        self.elapsed_time = ""
        self.remaining_time = ""
        self.current_epoch = 0

        self.stop = False
        self.learning = False

    def run(self):
        self.stop = False

        self.learning = True
        print("Learning started")

        with sess.graph.as_default():
            model, df = learn(self.size, self.epochs, self.memory_size, self.batch_size, self.model, thread=self)
            hex_io.save_model_and_df(model, df, self.size, self.epochs, self.memory_size, self.batch_size, self.comment)

        self.learning = False
        print("Learning ended")

    def get_progress(self):
        """
        Return progress of the learning
        :return: float between 0 and 1
        """
        return self.current_epoch / self.epochs

    def get_plot(self):
        n = self.current_epoch
        k = n // 25

        player = np.zeros(25)
        error = np.zeros(25)
        loss = np.zeros(25)
        index = np.zeros(25)

        for i in range(25):
            index[i] = k * i
            loss[i] = self.loss_array[k * i:k * (i + 1)].mean()

            w = self.winner_array[k * i:(k * (i + 1))]
            player[i] = (w == 1).sum() / k * 100
            error[i] = (w == 2).sum() / k * 100
        return index, player, error, loss

    def set_epoch(self, epoch):
        """
        Set epoch of the training
        :param epoch: epoch
        """
        if self.start_time == -1:
            self.start_time = datetime.datetime.now()

        self.current_epoch = epoch

        elapsed = int((datetime.datetime.now() - self.start_time).seconds)
        total = int(elapsed * self.epochs / (epoch + 1))

        self.remaining_time = datetime.timedelta(seconds=max(total - elapsed, 0))
        self.elapsed_time = datetime.timedelta(seconds=elapsed)

        print("Current epoch: {}; Remaining time: {}; Elapsed time: {}".format(
            self.current_epoch, self.remaining_time, self.elapsed_time))
