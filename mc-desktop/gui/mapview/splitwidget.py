import os, sys
from PyQt5 import QtCore, QtWidgets
from helper import timehelper
from database import dbupdates
from gui.style import styleparser


class SplitWidget(QtWidgets.QFrame):
    def __init__(self, mapview, movementId, pathdictlistwithtime, appStatus, dbConnection):
        QtWidgets.QFrame.__init__(self)
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.setToolTip("Split this movement, if you want to specify different travel modes for parts of it.")
        stylesheetFilename = 'sliderstylesheet.css'
        processedstylesheetPath = styleparser.preprocessStylesheet(stylesheetFilename)
        with open(processedstylesheetPath, 'r', encoding='utf-8') as file:
            processedstylesheet = file.read()
            self.setStyleSheet(processedstylesheet)

        # properties needed in case of a split event
        self.currentTimestamp = None
        self.movementId = movementId

        self.splitButton = QtWidgets.QPushButton("Split")
        self.splitSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.splitTime = QtWidgets.QLabel("time")

        gridlayout = QtWidgets.QGridLayout()
        gridlayout.addWidget(self.splitButton, 1, 0)
        gridlayout.addWidget(self.splitTime, 0, 1)
        gridlayout.addWidget(self.splitSlider, 1, 1)
        gridlayout.setAlignment(self.splitTime, QtCore.Qt.AlignCenter)
        self.setLayout(gridlayout)

        # splitButton setup
        self.splitButton.setEnabled(False)
        self.splitButton.clicked.connect(lambda: mapview.splitSignal.emit(appStatus, dbConnection, movementId, self.currentTimestamp))

        # splitSlider setup
        self.splitSlider.setMinimum(0)
        self.splitSlider.setMaximum(len(pathdictlistwithtime) - 1)
        self.splitSlider.setSingleStep(1)
        self.updateSplitTimeText(pathdictlistwithtime[0]['time'])

        self.splitSlider.valueChanged.connect(self.manageEnabelingOfSplitButton)
        # place a splitMarker for current sliderValue
        self.splitSlider.valueChanged.connect(lambda: mapview.showSplitMarker(pathdictlistwithtime[self.splitSlider.value()]['pathdictpoint']))
        # set time in splitTime according to current sliderValue
        self.splitSlider.valueChanged.connect(lambda: self.updateSplitTimeText(pathdictlistwithtime[self.splitSlider.value()]['time']))

    def updateSplitTimeText(self, timestamp):
        self.currentTimestamp = timestamp
        currentSliderTime = timehelper.timestamp_to_utc(timestamp).time()
        currentSliderTime = QtCore.QTime(currentSliderTime).toString('hh:mm')
        self.splitTime.setText(currentSliderTime)

    def manageEnabelingOfSplitButton(self, sliderValue):
        bool = self.splitSlider.minimum() < sliderValue < self.splitSlider.maximum()
        self.splitButton.setEnabled(bool)