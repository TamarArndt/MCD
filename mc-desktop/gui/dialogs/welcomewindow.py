import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from helper.filehelper import FileHelper


class WelcomeDialog(QtWidgets.QDialog):
    def __init__(self, appStatus):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.setWindowTitle("Welcome")
        PROJECT_DIR = FileHelper().get_project_cwd()
        self.setWindowIcon(QtGui.QIcon(os.path.join(PROJECT_DIR, 'res', 'mc-logo.svg')))
        self.setModal(True)
        self.setMinimumWidth(550)

        logo = QtSvg.QSvgWidget(os.path.join(PROJECT_DIR, 'res', 'mc-logo.svg'))
        logo.setFixedSize(80, 80)

        text = QtWidgets.QTextEdit()

        content = "<h1>Welcome to the desktop version of the Mobility Companion!</h1>" \
                  "<p>We are pleased to have you here.</p>" \
                  "<p>With this application you can label data that was logged by the Mobility Companion Android/iOS application." \
                  "<p>Check out the settings menu for... "

        text.textCursor().insertHtml(content)
        # text.setMinimumSize(QtCore.QSize(480, 340))

        # TODO checkbox: don't show this on startup anymore

        okButton = QtWidgets.QPushButton('Ok')
        okButton.setObjectName('okButton')
        okButton.clicked.connect(self.accept)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setSpacing(20)
        hlayout.addWidget(logo, 1)
        hlayout.setAlignment(logo, QtCore.Qt.AlignTop)
        hlayout.addWidget(text, 2)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(10, 10, 10, 10)
        vlayout.setSpacing(20)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(okButton, 1)
        vlayout.setAlignment(logo, QtCore.Qt.AlignCenter)
        vlayout.setAlignment(okButton, QtCore.Qt.AlignRight)
        self.setLayout(vlayout)
