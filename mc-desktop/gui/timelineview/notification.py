import os, sys
from PyQt5 import QtCore, QtWidgets
from gui.style import styleparser

class Notification(QtWidgets.QLabel):
    def __init__(self, labelingStatusForCurrentDate):
        QtWidgets.QLabel.__init__(self)
        self.setAlignment(QtCore.Qt.AlignCenter)
        stylesheetFilename = 'notificationstylesheet.css'
        processedstylesheetPath = styleparser.preprocessStylesheet(stylesheetFilename)
        with open(processedstylesheetPath, 'r', encoding='utf-8') as file:
            processedstylesheet = file.read()
            self.setStyleSheet(processedstylesheet)
        size = QtWidgets.QLabel('x')
        self.setFixedHeight(size.sizeHint().height() * 6)

        self.setProperty('status', 'noEntries')
        self.setContent(labelingStatusForCurrentDate)

    def setContent(self, labelingStatusForCurrentDate):
        totalNumberOfEntries = labelingStatusForCurrentDate.totalNumberOfStops + labelingStatusForCurrentDate.totalNumberOfMovements
        if totalNumberOfEntries == 0:
            self.noEntriesForThisDateNotification()
        else:
            self.labelingStatusNotification(labelingStatusForCurrentDate)

        # update style
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def noEntriesForThisDateNotification(self):
        self.setProperty('status', 'noEntries')
        text = "<strong> We are deeply sorry! </strong><br>"
        text += "There are no detected trips for this date."
        self.setText(text)

    def labelingStatusNotification(self, labelingStatus):
        numberOfUnlabeledStops = labelingStatus.totalNumberOfStops - labelingStatus.numberOfLabeledStops
        numberOfUnlabeledMovements = labelingStatus.totalNumberOfMovements - labelingStatus.numberOfLabeledMovements

        if numberOfUnlabeledStops == 0 and numberOfUnlabeledMovements == 0:
            self.setProperty('status', 'fullyLabeled')
            text = "<strong> Thank you for labeling with us! </strong><br>"
            text += "All entries of this date seem to be labeled."
        else:
            self.setProperty('status', 'partiallyLabeled')
            text = "<strong> Here is your detected timeline. </strong><br>"
            # Stops
            if numberOfUnlabeledStops == 0:
                text += "You have labeled all stops of this date. <br>"
            else:
                text += "Please label the remaining " + str(numberOfUnlabeledStops) + " stops. <br>"
            # Movements
            if numberOfUnlabeledMovements == 0:
                text += "Your have labeled all movements of this date."
            else:
                text += "Please label the remaining " + str(numberOfUnlabeledMovements) + " movements."

        self.setText(text)
