import os, sys
from PyQt5 import QtGui, QtWidgets


class ShortcutWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)

        # window settings
        self.setWindowTitle("Shortcuts")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg')))
        self.setFixedHeight(400)
        self.setFixedWidth(400)

        # content
        overview = QtWidgets.QWidget()
        # TODO image ShortcutOverview

        shortcut_layout = QtWidgets.QVBoxLayout()
        shortcut_layout.setContentsMargins(0, 0, 0, 0)
        shortcut_layout.addWidget(overview)
        self.setLayout(shortcut_layout)