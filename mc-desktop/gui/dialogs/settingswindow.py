import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from helper.filehelper import FileHelper

class SettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)

        # window settings
        self.setWindowTitle("About Mobility Companion Desktop")
        PROJECT_DIR = FileHelper().get_project_cwd()
        self.setWindowIcon(QtGui.QIcon(os.path.join(PROJECT_DIR, 'res', 'mc-logo.svg')))
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        self.setFixedHeight(screen.height()/2)
        self.setFixedWidth(screen.width()/3)

        logo = QtSvg.QSvgWidget(os.path.join(PROJECT_DIR, 'res', 'mc-logo.svg'))
        logo.setFixedSize(100, 100)
        aboutText = QtWidgets.QTextEdit()

        content = "<h1 align=center> Mobility Companion Desktop </h1>" \
                  " <p align=center style='line-height: 120%;'> This application is an extension to the <i> Mobility Companion </i> Android App." \
                  " The data collected by the Mobility Companion app can be viewed and labeled with" \
                  " <i>Mobility Companion Desktop</i>." \
                  " Its' main purpose is to facilitate the labeling process. </p>"
        aboutText.textCursor().insertHtml(content)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(logo, 1)
        layout.setAlignment(logo, QtCore.Qt.AlignCenter)
        layout.addWidget(aboutText, 2)
        self.setLayout(layout)
