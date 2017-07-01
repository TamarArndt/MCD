import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)

        # window settings
        self.setWindowTitle("about Mobility Companion Desktop")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/mc-logo.svg')))

        # position window centered on screen
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        screencenter = screen.center()
        self.setGeometry(0, 0, screen.width()/3, screen.height()/2)
        geom = self.frameGeometry()
        geom.moveCenter(screencenter)
        self.move(geom.topLeft())

        logo = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/mc-logo.svg'))
        logo.setFixedSize(100, 100)
        aboutText = AboutInfo()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(logo, 1)
        layout.setAlignment(logo, QtCore.Qt.AlignCenter)
        layout.addWidget(aboutText, 2)
        self.setLayout(layout)


class AboutInfo(QtWidgets.QTextEdit):
    def __init__(self):
        QtWidgets.QTextEdit.__init__(self)

        self.setReadOnly(True)
        self.setWordWrapMode(True)

        self.setStyleSheet("QTextEdit {font-size: 12.5pt;}")
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.viewport().setAutoFillBackground(False)

        content = "<h1 align=center> Mobility Companion Desktop </h1>" \
                  " <p align=center style='line-height: 120%;'> This application is an extension to the <i> Mobility Companion </i> Android App." \
                  " The data collected by the Mobility Companion app can be viewed and labeled with" \
                  " <i>Mobility Companion Desktop</i>." \
                  " Its' main purpose is to facilitate the labeling process. </p>"


        self.textCursor().insertHtml(content)
