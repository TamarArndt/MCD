import os, sys
from PyQt5 import QtGui, QtWidgets


class ShortcutWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)

        # window settings
        self.setWindowTitle("shortcut overview")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/mc-logo.svg')))

        # position window centered on screen
        screencenter = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.setGeometry(0, 0, 400, 400)
        geom = self.frameGeometry()
        geom.moveCenter(screencenter)
        self.move(geom.topLeft())

        # content
        overview = QtWidgets.QWidget()
        # TODO image ShortcutOverview

        shortcut_layout = QtWidgets.QVBoxLayout()
        shortcut_layout.setContentsMargins(0, 0, 0, 0)
        shortcut_layout.addWidget(overview)
        self.setLayout(shortcut_layout)