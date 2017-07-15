from PyQt5 import QtCore, QtGui, QtWidgets


class TimelineHeader(QtWidgets.QFrame):
    def __init__(self, appStatus):
        QtWidgets.QFrame.__init__(self)
        self.appStatus = appStatus

        self.dateLabel = DateLabel(appStatus)
        self.dateDecrement = QtWidgets.QToolButton()
        self.dateIncrement = QtWidgets.QToolButton()
        self.dateDecrement.setArrowType(QtCore.Qt.LeftArrow)
        self.dateIncrement.setArrowType(QtCore.Qt.RightArrow)
        self.dateDecrement.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.dateIncrement.setFocusPolicy(QtCore.Qt.ClickFocus)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setSpacing(0)
        hlayout.addWidget(self.dateDecrement)
        hlayout.addWidget(self.dateLabel)
        hlayout.addWidget(self.dateIncrement)
        hlayout.setAlignment(self.dateLabel, QtCore.Qt.AlignCenter)
        self.setLayout(hlayout)

        self.dateDecrement.pressed.connect(lambda: self.dateLabelChange(False))
        self.dateIncrement.pressed.connect(lambda: self.dateLabelChange(True))

    def updateDateLabel(self, date):
        """ to be called from mainpage when calendar changed """
        self.dateLabel.updateLabel(date)

    def dateLabelChange(self, increment):
        newday = self.dateLabel.currentDate

        # set to next day if increment
        if increment and newday < self.dateLabel.maximumDate:
            newday = newday.addDays(1)
        # set to previous day if decrement
        elif not increment and newday > self.dateLabel.minimumDate:
            newday = newday.addDays(-1)
        else:
            return

        self.dateLabel.currentDate = newday
        self.dateLabel.updateDateLabel(newday)
        self.dateLabel.speak.emit(newday)


class DateLabel(QtWidgets.QLabel):
    speak = QtCore.pyqtSignal(QtCore.QDate)
    def __init__(self, appStatus):
        QtWidgets.QLabel.__init__(self)

        self.minimumDate = QtCore.QDate(appStatus.databaseRange_utc[0])
        self.maximumDate = QtCore.QDate(appStatus.databaseRange_utc[1])

        self.currentDate = QtCore.QDate(appStatus.currentDate)
        self.setText(self.currentDate.toString(QtCore.Qt.DefaultLocaleLongDate))

    def updateDateLabel(self, date):
        self.currentDate = QtCore.QDate(date)
        self.setText(self.currentDate.toString(QtCore.Qt.DefaultLocaleLongDate))
