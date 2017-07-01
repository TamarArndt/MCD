import os, sys
from PyQt5 import QtCore, QtWidgets
from helper import timehelper

class SplitWidget(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.setToolTip("Split this movement, if you want to specify different travel modes for parts of it.")

        self.splitButton = QtWidgets.QPushButton("Split")
        self.splitSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.splitTime = QtWidgets.QLabel("time")

        gridlayout = QtWidgets.QGridLayout()
        gridlayout.addWidget(self.splitButton, 1, 0)
        gridlayout.addWidget(self.splitTime, 0, 1)
        gridlayout.addWidget(self.splitSlider, 1, 1)
        gridlayout.setAlignment(self.splitTime, QtCore.Qt.AlignCenter)
        self.setLayout(gridlayout)

        self.splitButton.setEnabled(False)

        with open(os.path.join(os.path.dirname(sys.modules['__main__'].__file__) , './gui/style/sliderstylesheet.css'), 'r', encoding='utf-8') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

            # TODO add timelabel above slider that shows time at corresponding pathpoint

    def setUp(self, mapview, pathdictlistwithtime):
        ''' the slider is set up to represent the given path '''
        # TODO need to reset SplitSlider/complete SplitWidget! xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # remove and create new one
        # remove function: check if there is one, if yes: remove from layout
        # add: check if there is one, if no: add, else: remove and add

        self.splitSlider.setMinimum(0)
        self.splitSlider.setMaximum(len(pathdictlistwithtime) - 1)
        self.splitSlider.setSingleStep(1)
        self.updateSplitTimeText(pathdictlistwithtime[0]['time'])


        print(len(pathdictlistwithtime))
        print(self.splitSlider.maximum())

        self.splitSlider.valueChanged.connect(lambda: print(self.splitSlider.value()))
        self.splitSlider.valueChanged.connect(self.manageEnabelingOfSplitButton)
        # place a splitMarker for current sliderValue
        self.splitSlider.valueChanged.connect(lambda: mapview.showSplitMarker(pathdictlistwithtime[self.splitSlider.value()]['pathdictpoint']))
        # set time in splitTime according to current sliderValue
        self.splitSlider.valueChanged.connect(lambda: self.updateSplitTimeText(pathdictlistwithtime[self.splitSlider.value()]['time']))

        # if splitSlider not at min or max: enable splitButton

        # TODO with the slider movement also renew the time display


        #             # splitwidget setup
        #             self.splitwidget.split_slider.setMinimum(0)
        #             self.splitwidget.split_slider.setMaximum(len(self.dictlist) -1)
        #             self.splitwidget.split_slider.setSingleStep(1)
        #             self.splitwidget.split_slider.valueChanged.connect(self.split)
        #
        #             # create new markerItem (splitMarker) at minimumposition (in different color)
        #

    def updateSplitTimeText(self, timestamp):
        currentSliderTime = timehelper.timestamp_to_utc(timestamp).time()
        currentSliderTime = QtCore.QTime(currentSliderTime).toString('hh:mm')
        self.splitTime.setText(currentSliderTime)

    def manageEnabelingOfSplitButton(self, sliderValue):
        bool = self.splitSlider.minimum() < sliderValue < self.splitSlider.maximum()
        self.splitButton.setEnabled(bool)