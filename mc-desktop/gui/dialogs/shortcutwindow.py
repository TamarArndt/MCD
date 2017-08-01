import os, sys
from PyQt5 import QtGui, QtWidgets
from helper.filehelper import FileHelper


class ShortcutWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)

        # window settings
        self.setWindowTitle("Shortcuts")
        PROJECT_DIR = FileHelper().get_project_cwd()
        self.setWindowIcon(QtGui.QIcon(os.path.join(PROJECT_DIR, 'res', 'mc-logo.svg')))
        self.setFixedHeight(400)
        self.setFixedWidth(400)

        # content
        overview = QtWidgets.QWidget()
        # TODO image ShortcutOverview

        shortcut_layout = QtWidgets.QVBoxLayout()
        shortcut_layout.setContentsMargins(0, 0, 0, 0)
        shortcut_layout.addWidget(overview)
        self.setLayout(shortcut_layout)