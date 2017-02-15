from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from hex_game.graphics.plots import TrainPlot
from hex_game import hex_io
from hex_game.graphics.mainwindow import Ui_TIPE
from hex_game.threads.learn_thread import LearnThread


class TrainUI:
    def __init__(self, ui: Ui_TIPE):
        self.ui = ui
        self.create_plot()
        self.widgetPlot = self.ui.widgetTrainPlot

        # Connect update save folder
        self.ui.tabWidgetTrainChoice.currentChanged.connect(self.update_save_name)
        self.ui.spinBoxSizeTrain.valueChanged.connect(self.update_save_name)
        self.ui.doubleSpinBoxGamma.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxEpochs.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxEpochs.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxRandomEpochs.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxAdditionalEpochs.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxBatchSize.valueChanged.connect(self.update_save_name)

        self.last_index = 0
        self.model = ""
        self.thread = None  # type: LearnThread

        self.ui.pushButtonLoadModel.pressed.connect(self.load)
        self.ui.pushButtonTrain.pressed.connect(self.train_button)

        self.update_save_name()
        self.set_progress(-1)

        # Timer
        timer = QTimer(self.ui.centralWidget)
        timer.timeout.connect(self.update_train)
        timer.start(500)

    def create_plot(self):
        """
        Create the plot widget
        """
        self.ui.verticalLayoutTrainTab.removeWidget(self.ui.widgetTrainPlot)

        self.ui.widgetTrainPlot.deleteLater()

        self.ui.widgetTrainPlot = TrainPlot(self.ui.resultsTab, width=5, height=5, dpi=100)
        self.ui.widgetTrainPlot.setObjectName("widgetPlot")
        self.ui.verticalLayoutTrainTab.addWidget(self.ui.widgetTrainPlot)

    def update_plots(self):
        """
        Update the plots
        """
        if self.thread.index != self.last_index:
            self.last_index = self.thread.index

            # Clear
            self.widgetPlot.clear()

            # Plot
            self.widgetPlot.loss.plot(self.thread.epoch_log[:self.thread.index],
                                      self.thread.loss_log[:self.thread.index], 'o-')
            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        self.thread.player0_log[:self.thread.index], 'v-')
            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        self.thread.player1_log[:self.thread.index], 'o-')
            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        self.thread.error_log[:self.thread.index], 'P-')

            # Draw
            self.widgetPlot.draw()

    def set_progress(self, value, text=None):
        """
        Set Train progress bar value and text
        :param value: float between 0 and 1, negative to hide the bar
        :param text: text to display on the bar
        """
        if value < 0:
            self.ui.progressBarTrain.hide()
        else:
            self.ui.progressBarTrain.show()
            self.ui.progressBarTrain.setValue(100 * value)
            if text is not None:
                self.ui.progressBarTrain.setFormat(text)

    def load(self):
        """
        Open file dialog to load model to continue training
        """
        f, g = QFileDialog.getOpenFileName(self.ui.centralWidget, "Open file", "", "Model (*.model)")

        if f != "":
            self.model = f
            try:
                self.get_parameters()
            except ValueError:
                self.model = ""
                msg_box = QMessageBox()
                msg_box.setText("Bad naming")
                msg_box.setWindowTitle("Error")
                msg_box.exec_()
            self.ui.lineEditOldModel.setText(self.model)

    def train_button(self):
        """
        Handle train button click
        """
        if self.thread is None or not self.thread.learning:
            self.train()
        else:
            self.thread.stop = True

    def update_save_name(self):
        """
        Update save file name
        :return:
        """
        # Gamma approximation error fix
        self.ui.doubleSpinBoxGamma.setValue(round(self.ui.doubleSpinBoxGamma.value(), 2))
        self.ui.lineEditSaveName.setText(hex_io.save_dir + hex_io.get_save_name(*self.get_parameters()))

    def get_parameters(self):
        """
        Get the parameters for train
        :return: size, gamma, start_epoch, end_epoch, random_epochs, batch_size, part
        """
        if self.model == "":
            return self.ui.spinBoxSizeTrain.value(), \
                   self.ui.doubleSpinBoxGamma.value(), \
                   0, \
                   self.ui.spinBoxEpochs.value(), \
                   self.ui.spinBoxRandomEpochs.value(), \
                   self.ui.spinBoxBatchSize.value(), \
                   0
        else:
            size, gamma, start_epoch, end_epoch, random_epochs, batch_size, part = hex_io.get_parameters(self.model)
            start_epoch = end_epoch
            end_epoch += self.ui.spinBoxAdditionalEpochs.value()
            part += 1
            return size, gamma, start_epoch, end_epoch, random_epochs, batch_size, part

    def set_busy(self, busy):
        """
        Enable / Disable UI
        :param busy: budy
        """
        b = not busy
        self.ui.playTab.setEnabled(b)
        self.ui.resultsTab.setEnabled(b)
        self.ui.tabWidgetTrainChoice.setEnabled(b)
        self.ui.tabWidgetTrainChoice.setEnabled(b)
        self.ui.actionOpen.setEnabled(b)
        self.ui.menuBar.setEnabled(b)

        if busy:
            self.ui.pushButtonTrain.setText("Stop")
        else:
            self.ui.pushButtonTrain.setText("Train")

    def update_train(self):
        """
        Update function called every 500ms
        """
        if self.thread is None:
            return
        self.update_plots()
        text = "Elapsed: {} | Remaining: {}".format(self.thread.elapsed_time, self.thread.remaining_time)
        self.set_progress(self.thread.get_progress(), text)
        if not self.thread.learning:
            self.end_thread()

    def train(self):
        """
        Start training
        """
        size, gamma, start_epoch, end_epoch, random_epochs, batch_size, part = self.get_parameters()
        epsilon = self.ui.checkBoxResetEpsilon.isChecked()
        self.thread = LearnThread(size, gamma, start_epoch, end_epoch, random_epochs, self.model, epsilon, batch_size,
                                  part)
        self.thread.start()
        self.set_busy(True)

    def end_thread(self):
        """
        Save model and quit thread
        """
        self.set_busy(False)
        self.set_progress(1, "Done")
        self.thread.save()
        self.thread = None
