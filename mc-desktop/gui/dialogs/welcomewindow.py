import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

class WelcomeDialog(QtWidgets.QDialog):
    def __init__(self, appStatus):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg')))
        self.setModal(True)
        self.setMinimumWidth(550)

        logo = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg'))
        logo.setFixedSize(80, 80)

        welcome = QtWidgets.QLabel('<h2>Welcome to the Mobility Companion Desktop Application</h2>')


        info = 'Usertest mode: '
        if appStatus.usertestMode:
            info += 'On \n'
        else:
            info += 'Off \n'
        info += 'Adaptivity mode: '
        if appStatus.adaptivityMode:
            info += 'On'
        else:
            info += 'Off'

        okButton = QtWidgets.QPushButton('Ok')
        okButton.setObjectName('okButton')
        okButton.clicked.connect(self.accept)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(welcome)
        vlayout.addWidget(logo)
        vlayout.addWidget(QtWidgets.QLabel(info))
        vlayout.addWidget(okButton)

        vlayout.setAlignment(welcome, QtCore.Qt.AlignCenter)
        vlayout.setAlignment(logo, QtCore.Qt.AlignCenter)
        vlayout.setAlignment(okButton, QtCore.Qt.AlignRight)
        self.setLayout(vlayout)


        # maybe checkbox: don't show this on startup?


        welcometext = 'This application is for labeling data logged by the Mobility Companion Android/iOS Application.' \
                      'The system will try to help you labeling your data. ...'
