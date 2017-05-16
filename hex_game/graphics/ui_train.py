import numpy
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
        self.ui.spinBoxSizeTrain.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxBatchSize.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxMemory.valueChanged.connect(self.update_save_name)

        self.ui.checkBoxLoad.clicked.connect(self.check_box_load)

        self.last_index = 0
        self.model = ""
        self.thread = None  # type: LearnThread

        self.ui.pushButtonChoose.pressed.connect(self.choose_player)
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
                                      self.thread.loss_log[:self.thread.index], 'v-')
            self.widgetPlot.loss.set_ybound(0, numpy.nanmax(self.thread.loss_log))

            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        100 - self.thread.error_log[:self.thread.index], 'P-')
            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        self.thread.error_log[:self.thread.index], 'o-')
            self.widgetPlot.winner.set_ybound(0, 100)

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

    def choose_player(self):
        """
        Open file dialog to load model to continue training
        """
        f, g = QFileDialog.getOpenFileName(self.ui.centralWidget, "Open file", "", "Model (*.model)")

        if f != "":
            self.model = f
            try:
                hex_io.get_parameters(self.model)
            except ValueError:
                self.model = ""
                msg_box = QMessageBox()
                msg_box.setText("Bad naming")
                msg_box.setWindowTitle("Error")
                msg_box.exec_()
                self.ui.lineEditLoad.setText(self.model)
        self.check_box_load()

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
        """
        self.ui.lineEditSaveName.setText(hex_io.save_dir + hex_io.get_save_name(*self.get_parameters()))

    def check_box_load(self):
        checked = self.ui.checkBoxLoad.isChecked()

        self.ui.spinBoxSizeTrain.setEnabled(not checked)
        self.ui.spinBoxMemory.setEnabled(not checked)
        self.ui.spinBoxBatchSize.setEnabled(not checked)

        if checked and self.model != "":
            d = hex_io.get_parameters_dict(self.model)
            self.ui.spinBoxSizeTrain.setValue(d["size"])
            self.ui.spinBoxEpochs.setValue(d["epochs"])
            self.ui.spinBoxMemory.setValue(d["memory_size"])
            self.ui.spinBoxBatchSize.setValue(d["batch_size"])
            self.update_save_name()

    def get_parameters(self):
        """
        Get the parameters for train
        :return: size, epochs, memory_size, batch_size, comment
        """
        return self.ui.spinBoxSizeTrain.value(), self.ui.spinBoxEpochs.value(), self.ui.spinBoxMemory.value(), \
               self.ui.spinBoxBatchSize.value(), self.ui.lineEditComment.text()

    def set_busy(self, busy):
        """
        Enable / Disable UI
        :param busy: budy
        """
        b = not busy
        self.ui.playTab.setEnabled(b)
        self.ui.resultsTab.setEnabled(b)
        self.ui.actionOpen.setEnabled(b)
        self.ui.horizontalLayoutInput.setEnabled(b)
        self.ui.horizontalLayoutLoad.setEnabled(b)
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
        self.thread = LearnThread(*self.get_parameters(), self.model)
        self.thread.start()
        self.set_busy(True)

    def end_thread(self):
        """
        Save model and quit thread
        """
        self.set_busy(False)
        self.set_progress(1, "Done")
        self.thread.join()
        self.thread = None
