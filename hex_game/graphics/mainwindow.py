# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TIPE_Hex_QT/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TIPE(object):
    def setupUi(self, TIPE):
        TIPE.setObjectName("TIPE")
        TIPE.resize(766, 805)
        self.centralWidget = QtWidgets.QWidget(TIPE)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.playTab = QtWidgets.QWidget()
        self.playTab.setObjectName("playTab")
        self.horizontalLayoutPlayTab = QtWidgets.QHBoxLayout(self.playTab)
        self.horizontalLayoutPlayTab.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayoutPlayTab.setSpacing(6)
        self.horizontalLayoutPlayTab.setObjectName("horizontalLayoutPlayTab")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBarMinimax = QtWidgets.QProgressBar(self.playTab)
        self.progressBarMinimax.setEnabled(True)
        self.progressBarMinimax.setProperty("value", 0)
        self.progressBarMinimax.setObjectName("progressBarMinimax")
        self.gridLayout.addWidget(self.progressBarMinimax, 9, 0, 1, 1)
        self.plainTextEditDebugPlay = QtWidgets.QPlainTextEdit(self.playTab)
        self.plainTextEditDebugPlay.setReadOnly(True)
        self.plainTextEditDebugPlay.setObjectName("plainTextEditDebugPlay")
        self.gridLayout.addWidget(self.plainTextEditDebugPlay, 13, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.horizontalLayoutView = QtWidgets.QHBoxLayout()
        self.horizontalLayoutView.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayoutView.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayoutView.setSpacing(6)
        self.horizontalLayoutView.setObjectName("horizontalLayoutView")
        self.labelView = QtWidgets.QLabel(self.playTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelView.sizePolicy().hasHeightForWidth())
        self.labelView.setSizePolicy(sizePolicy)
        self.labelView.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelView.setObjectName("labelView")
        self.horizontalLayoutView.addWidget(self.labelView)
        self.pushButtonViewDefault = QtWidgets.QPushButton(self.playTab)
        self.pushButtonViewDefault.setCheckable(True)
        self.pushButtonViewDefault.setChecked(False)
        self.pushButtonViewDefault.setObjectName("pushButtonViewDefault")
        self.horizontalLayoutView.addWidget(self.pushButtonViewDefault)
        self.pushButtonViewPlayer1 = QtWidgets.QPushButton(self.playTab)
        self.pushButtonViewPlayer1.setCheckable(True)
        self.pushButtonViewPlayer1.setObjectName("pushButtonViewPlayer1")
        self.horizontalLayoutView.addWidget(self.pushButtonViewPlayer1)
        self.pushButtonViewPlayer2 = QtWidgets.QPushButton(self.playTab)
        self.pushButtonViewPlayer2.setCheckable(True)
        self.pushButtonViewPlayer2.setObjectName("pushButtonViewPlayer2")
        self.horizontalLayoutView.addWidget(self.pushButtonViewPlayer2)
        self.gridLayout.addLayout(self.horizontalLayoutView, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        self.formLayoutNewGame = QtWidgets.QFormLayout()
        self.formLayoutNewGame.setContentsMargins(11, 11, 11, 11)
        self.formLayoutNewGame.setSpacing(6)
        self.formLayoutNewGame.setObjectName("formLayoutNewGame")
        self.labelPlayer1 = QtWidgets.QLabel(self.playTab)
        self.labelPlayer1.setObjectName("labelPlayer1")
        self.formLayoutNewGame.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelPlayer1)
        self.comboBoxPlayer1 = QtWidgets.QComboBox(self.playTab)
        self.comboBoxPlayer1.setObjectName("comboBoxPlayer1")
        self.formLayoutNewGame.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxPlayer1)
        self.labelMinimaxDepthPlayer1 = QtWidgets.QLabel(self.playTab)
        self.labelMinimaxDepthPlayer1.setObjectName("labelMinimaxDepthPlayer1")
        self.formLayoutNewGame.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelMinimaxDepthPlayer1)
        self.spinBoxMinimaxDepthPlayer1 = QtWidgets.QSpinBox(self.playTab)
        self.spinBoxMinimaxDepthPlayer1.setMinimum(1)
        self.spinBoxMinimaxDepthPlayer1.setObjectName("spinBoxMinimaxDepthPlayer1")
        self.formLayoutNewGame.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBoxMinimaxDepthPlayer1)
        self.labelPlayer2 = QtWidgets.QLabel(self.playTab)
        self.labelPlayer2.setObjectName("labelPlayer2")
        self.formLayoutNewGame.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelPlayer2)
        self.comboBoxPlayer2 = QtWidgets.QComboBox(self.playTab)
        self.comboBoxPlayer2.setObjectName("comboBoxPlayer2")
        self.formLayoutNewGame.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBoxPlayer2)
        self.labelMinimaxDepthPlayer2 = QtWidgets.QLabel(self.playTab)
        self.labelMinimaxDepthPlayer2.setObjectName("labelMinimaxDepthPlayer2")
        self.formLayoutNewGame.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.labelMinimaxDepthPlayer2)
        self.spinBoxMinimaxDepthPlayer2 = QtWidgets.QSpinBox(self.playTab)
        self.spinBoxMinimaxDepthPlayer2.setMinimum(1)
        self.spinBoxMinimaxDepthPlayer2.setObjectName("spinBoxMinimaxDepthPlayer2")
        self.formLayoutNewGame.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spinBoxMinimaxDepthPlayer2)
        self.pushButtonNewGame = QtWidgets.QPushButton(self.playTab)
        self.pushButtonNewGame.setObjectName("pushButtonNewGame")
        self.formLayoutNewGame.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pushButtonNewGame)
        self.gridLayout.addLayout(self.formLayoutNewGame, 5, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 16, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 0, 1, 1)
        self.pushButtonPlay = QtWidgets.QPushButton(self.playTab)
        self.pushButtonPlay.setObjectName("pushButtonPlay")
        self.gridLayout.addWidget(self.pushButtonPlay, 7, 0, 1, 1)
        self.listWidgetModels = QtWidgets.QListWidget(self.playTab)
        self.listWidgetModels.setObjectName("listWidgetModels")
        item = QtWidgets.QListWidgetItem()
        self.listWidgetModels.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetModels.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetModels.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetModels.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetModels.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetModels.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetModels.addItem(item)
        self.gridLayout.addWidget(self.listWidgetModels, 11, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 8, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 6, 0, 1, 1)
        self.formLayoutSize = QtWidgets.QFormLayout()
        self.formLayoutSize.setContentsMargins(11, 11, 11, 11)
        self.formLayoutSize.setSpacing(6)
        self.formLayoutSize.setObjectName("formLayoutSize")
        self.labelSize = QtWidgets.QLabel(self.playTab)
        self.labelSize.setObjectName("labelSize")
        self.formLayoutSize.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelSize)
        self.spinBoxSizePlay = QtWidgets.QSpinBox(self.playTab)
        self.spinBoxSizePlay.setMinimum(2)
        self.spinBoxSizePlay.setObjectName("spinBoxSizePlay")
        self.formLayoutSize.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxSizePlay)
        self.gridLayout.addLayout(self.formLayoutSize, 3, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 12, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 10, 0, 1, 1)
        self.horizontalLayoutPlayTab.addLayout(self.gridLayout)
        self.graphicsViewDefault = QtWidgets.QGraphicsView(self.playTab)
        self.graphicsViewDefault.setEnabled(True)
        self.graphicsViewDefault.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.graphicsViewDefault.setObjectName("graphicsViewDefault")
        self.horizontalLayoutPlayTab.addWidget(self.graphicsViewDefault)
        self.graphicsViewPlayer1 = QtWidgets.QGraphicsView(self.playTab)
        self.graphicsViewPlayer1.setEnabled(True)
        self.graphicsViewPlayer1.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.graphicsViewPlayer1.setObjectName("graphicsViewPlayer1")
        self.horizontalLayoutPlayTab.addWidget(self.graphicsViewPlayer1)
        self.graphicsViewPlayer2 = QtWidgets.QGraphicsView(self.playTab)
        self.graphicsViewPlayer2.setEnabled(True)
        self.graphicsViewPlayer2.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.graphicsViewPlayer2.setObjectName("graphicsViewPlayer2")
        self.horizontalLayoutPlayTab.addWidget(self.graphicsViewPlayer2)
        self.tabWidget.addTab(self.playTab, "")
        self.resultsTab = QtWidgets.QWidget()
        self.resultsTab.setObjectName("resultsTab")
        self.horizontalLayoutResultsTab = QtWidgets.QHBoxLayout(self.resultsTab)
        self.horizontalLayoutResultsTab.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayoutResultsTab.setSpacing(6)
        self.horizontalLayoutResultsTab.setObjectName("horizontalLayoutResultsTab")
        self.listWidgetResults = QtWidgets.QListWidget(self.resultsTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetResults.sizePolicy().hasHeightForWidth())
        self.listWidgetResults.setSizePolicy(sizePolicy)
        self.listWidgetResults.setObjectName("listWidgetResults")
        self.horizontalLayoutResultsTab.addWidget(self.listWidgetResults)
        self.verticalLayoutResults = QtWidgets.QVBoxLayout()
        self.verticalLayoutResults.setContentsMargins(11, 11, 11, 11)
        self.verticalLayoutResults.setSpacing(6)
        self.verticalLayoutResults.setObjectName("verticalLayoutResults")
        self.widgetResultsPlot = QtWidgets.QWidget(self.resultsTab)
        self.widgetResultsPlot.setObjectName("widgetResultsPlot")
        self.verticalLayoutResults.addWidget(self.widgetResultsPlot)
        self.widgetResultsToolbar = QtWidgets.QWidget(self.resultsTab)
        self.widgetResultsToolbar.setObjectName("widgetResultsToolbar")
        self.verticalLayoutResults.addWidget(self.widgetResultsToolbar)
        self.horizontalLayoutResultsTab.addLayout(self.verticalLayoutResults)
        self.tabWidget.addTab(self.resultsTab, "")
        self.trainTab = QtWidgets.QWidget()
        self.trainTab.setObjectName("trainTab")
        self.verticalLayoutTrainTab = QtWidgets.QVBoxLayout(self.trainTab)
        self.verticalLayoutTrainTab.setContentsMargins(11, 11, 11, 11)
        self.verticalLayoutTrainTab.setSpacing(6)
        self.verticalLayoutTrainTab.setObjectName("verticalLayoutTrainTab")
        self.formLayoutTrain = QtWidgets.QFormLayout()
        self.formLayoutTrain.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.formLayoutTrain.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayoutTrain.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayoutTrain.setContentsMargins(11, 11, 11, 11)
        self.formLayoutTrain.setSpacing(6)
        self.formLayoutTrain.setObjectName("formLayoutTrain")
        self.labelSaveFolder = QtWidgets.QLabel(self.trainTab)
        self.labelSaveFolder.setObjectName("labelSaveFolder")
        self.formLayoutTrain.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelSaveFolder)
        self.lineEditSaveFolder = QtWidgets.QLineEdit(self.trainTab)
        self.lineEditSaveFolder.setReadOnly(True)
        self.lineEditSaveFolder.setObjectName("lineEditSaveFolder")
        self.formLayoutTrain.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditSaveFolder)
        self.verticalLayoutTrainTab.addLayout(self.formLayoutTrain)
        self.tabWidgetTrainChoice = QtWidgets.QTabWidget(self.trainTab)
        self.tabWidgetTrainChoice.setObjectName("tabWidgetTrainChoice")
        self.tabNewTraining = QtWidgets.QWidget()
        self.tabNewTraining.setObjectName("tabNewTraining")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tabNewTraining)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.labelGamma = QtWidgets.QLabel(self.tabNewTraining)
        self.labelGamma.setObjectName("labelGamma")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelGamma)
        self.doubleSpinBoxGamma = QtWidgets.QDoubleSpinBox(self.tabNewTraining)
        self.doubleSpinBoxGamma.setMaximum(1.0)
        self.doubleSpinBoxGamma.setSingleStep(0.01)
        self.doubleSpinBoxGamma.setObjectName("doubleSpinBoxGamma")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxGamma)
        self.labelSize_2 = QtWidgets.QLabel(self.tabNewTraining)
        self.labelSize_2.setObjectName("labelSize_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelSize_2)
        self.spinBoxSizeTrain = QtWidgets.QSpinBox(self.tabNewTraining)
        self.spinBoxSizeTrain.setMinimum(2)
        self.spinBoxSizeTrain.setObjectName("spinBoxSizeTrain")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxSizeTrain)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(11, 11, 11, 11)
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelEpochs = QtWidgets.QLabel(self.tabNewTraining)
        self.labelEpochs.setObjectName("labelEpochs")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelEpochs)
        self.spinBoxEpochs = QtWidgets.QSpinBox(self.tabNewTraining)
        self.spinBoxEpochs.setMinimum(1000)
        self.spinBoxEpochs.setMaximum(999999999)
        self.spinBoxEpochs.setSingleStep(1000)
        self.spinBoxEpochs.setObjectName("spinBoxEpochs")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxEpochs)
        self.labelRandomEpochs = QtWidgets.QLabel(self.tabNewTraining)
        self.labelRandomEpochs.setObjectName("labelRandomEpochs")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelRandomEpochs)
        self.spinBoxRandomEpochs = QtWidgets.QSpinBox(self.tabNewTraining)
        self.spinBoxRandomEpochs.setMaximum(999999999)
        self.spinBoxRandomEpochs.setSingleStep(1000)
        self.spinBoxRandomEpochs.setObjectName("spinBoxRandomEpochs")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxRandomEpochs)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.tabWidgetTrainChoice.addTab(self.tabNewTraining, "")
        self.tabContinueTraining = QtWidgets.QWidget()
        self.tabContinueTraining.setObjectName("tabContinueTraining")
        self.formLayout_3 = QtWidgets.QFormLayout(self.tabContinueTraining)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setContentsMargins(11, 11, 11, 11)
        self.formLayout_3.setSpacing(6)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label = QtWidgets.QLabel(self.tabContinueTraining)
        self.label.setObjectName("label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lineEditOldModel = QtWidgets.QLineEdit(self.tabContinueTraining)
        self.lineEditOldModel.setReadOnly(True)
        self.lineEditOldModel.setObjectName("lineEditOldModel")
        self.horizontalLayout_4.addWidget(self.lineEditOldModel)
        self.pushButtonLoadModel = QtWidgets.QPushButton(self.tabContinueTraining)
        self.pushButtonLoadModel.setObjectName("pushButtonLoadModel")
        self.horizontalLayout_4.addWidget(self.pushButtonLoadModel)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_2 = QtWidgets.QLabel(self.tabContinueTraining)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBoxAdditionalEpochs = QtWidgets.QSpinBox(self.tabContinueTraining)
        self.spinBoxAdditionalEpochs.setMinimum(1000)
        self.spinBoxAdditionalEpochs.setMaximum(999999999)
        self.spinBoxAdditionalEpochs.setSingleStep(1000)
        self.spinBoxAdditionalEpochs.setObjectName("spinBoxAdditionalEpochs")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxAdditionalEpochs)
        self.tabWidgetTrainChoice.addTab(self.tabContinueTraining, "")
        self.verticalLayoutTrainTab.addWidget(self.tabWidgetTrainChoice)
        self.pushButtonTrain = QtWidgets.QPushButton(self.trainTab)
        self.pushButtonTrain.setObjectName("pushButtonTrain")
        self.verticalLayoutTrainTab.addWidget(self.pushButtonTrain)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutTrainTab.addItem(spacerItem8)
        self.progressBarTrain = QtWidgets.QProgressBar(self.trainTab)
        self.progressBarTrain.setProperty("value", 0)
        self.progressBarTrain.setTextVisible(True)
        self.progressBarTrain.setObjectName("progressBarTrain")
        self.verticalLayoutTrainTab.addWidget(self.progressBarTrain)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutTrainTab.addItem(spacerItem9)
        self.widgetTrainPlot = QtWidgets.QWidget(self.trainTab)
        self.widgetTrainPlot.setObjectName("widgetTrainPlot")
        self.verticalLayoutTrainTab.addWidget(self.widgetTrainPlot)
        self.tabWidget.addTab(self.trainTab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        TIPE.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(TIPE)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 766, 16))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        TIPE.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(TIPE)
        self.mainToolBar.setObjectName("mainToolBar")
        TIPE.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(TIPE)
        self.statusBar.setObjectName("statusBar")
        TIPE.setStatusBar(self.statusBar)
        self.actionOpen = QtWidgets.QAction(TIPE)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(TIPE)
        self.tabWidget.setCurrentIndex(2)
        self.tabWidgetTrainChoice.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TIPE)

    def retranslateUi(self, TIPE):
        _translate = QtCore.QCoreApplication.translate
        TIPE.setWindowTitle(_translate("TIPE", "MainWindow"))
        self.plainTextEditDebugPlay.setPlainText(_translate("TIPE", "THis is text"))
        self.labelView.setText(_translate("TIPE", "View"))
        self.pushButtonViewDefault.setText(_translate("TIPE", "Default"))
        self.pushButtonViewPlayer1.setText(_translate("TIPE", "Player 1"))
        self.pushButtonViewPlayer2.setText(_translate("TIPE", "Player 2"))
        self.labelPlayer1.setText(_translate("TIPE", "Player 1"))
        self.labelMinimaxDepthPlayer1.setText(_translate("TIPE", "Depth"))
        self.labelPlayer2.setText(_translate("TIPE", "Player 2"))
        self.labelMinimaxDepthPlayer2.setText(_translate("TIPE", "Depth"))
        self.pushButtonNewGame.setText(_translate("TIPE", "New Game"))
        self.pushButtonPlay.setText(_translate("TIPE", "Play"))
        __sortingEnabled = self.listWidgetModels.isSortingEnabled()
        self.listWidgetModels.setSortingEnabled(False)
        item = self.listWidgetModels.item(0)
        item.setText(_translate("TIPE", "test"))
        item = self.listWidgetModels.item(1)
        item.setText(_translate("TIPE", "azaz"))
        item = self.listWidgetModels.item(2)
        item.setText(_translate("TIPE", "azaz"))
        item = self.listWidgetModels.item(3)
        item.setText(_translate("TIPE", "dsfd"))
        item = self.listWidgetModels.item(4)
        item.setText(_translate("TIPE", "dfdf"))
        item = self.listWidgetModels.item(5)
        item.setText(_translate("TIPE", "qsd"))
        item = self.listWidgetModels.item(6)
        item.setText(_translate("TIPE", "&"))
        self.listWidgetModels.setSortingEnabled(__sortingEnabled)
        self.labelSize.setText(_translate("TIPE", "Size"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.playTab), _translate("TIPE", "Play"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resultsTab), _translate("TIPE", "Results"))
        self.labelSaveFolder.setText(_translate("TIPE", "Save folder"))
        self.labelGamma.setText(_translate("TIPE", "Gamma"))
        self.labelSize_2.setText(_translate("TIPE", "Size"))
        self.labelEpochs.setText(_translate("TIPE", "Epochs"))
        self.labelRandomEpochs.setText(_translate("TIPE", "Random Epochs"))
        self.tabWidgetTrainChoice.setTabText(self.tabWidgetTrainChoice.indexOf(self.tabNewTraining), _translate("TIPE", "New Training"))
        self.label.setText(_translate("TIPE", "Old model"))
        self.pushButtonLoadModel.setText(_translate("TIPE", "Load"))
        self.label_2.setText(_translate("TIPE", "Additional epochs"))
        self.tabWidgetTrainChoice.setTabText(self.tabWidgetTrainChoice.indexOf(self.tabContinueTraining), _translate("TIPE", "Continue Training"))
        self.pushButtonTrain.setText(_translate("TIPE", "Train"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trainTab), _translate("TIPE", "Train"))
        self.menuFile.setTitle(_translate("TIPE", "File"))
        self.actionOpen.setText(_translate("TIPE", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TIPE = QtWidgets.QMainWindow()
    ui = Ui_TIPE()
    ui.setupUi(TIPE)
    TIPE.show()
    sys.exit(app.exec_())

