from PyQt5 import QtWidgets


class Questionnaire(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        self.setStyleSheet('QFrame {background-color: #B1CCBA;} ')

        # if appStatus.usertestMode:
        #     dont try to find questionnaire stuff in database