from PyQt5 import QtCore, QtWidgets


class Notification(QtWidgets.QLabel):
    def __init__(self):
        QtWidgets.QLabel.__init__(self)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.noEntriesForThisDateNotification()

    def noEntriesForThisDateNotification(self):
        text = "<strong> We are deeply sorry! </strong><br>"
        text += "There are no detected trips for this date."
        self.setText(text)
        self.setStyleSheet("QLabel {background-color: #e6e6e6; }")

    def remainingEntriesNotification(self, numberOfUnlabeledEntries):
        text = "<strong> Here is your detected timeline. </strong><br>"
        text += "Please label the remaining " + str(numberOfUnlabeledEntries) + " entries."
        self.setText(text)
        self.setStyleSheet("QLabel {background-color: yellow; }")

    def dateFullyLabeledNotification(self):
        text = "<strong> Thank you for labeling with us! </strong><br>"
        text += "All entries of this date seem to be labeled."
        self.setText(text)
        self.setStyleSheet("QLabel {background-color: green; }")

