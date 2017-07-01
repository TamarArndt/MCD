import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import shortcutwindow, aboutwindow, mainpage


class MainWindow(QtWidgets.QMainWindow):
    """ MainWindow encapsulates menu, statusbar and mainPage (containing calendar-, timeline- and mapview)"""
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.appStatus = appStatus

        # set Window
        self.setWindowTitle("Mobility Companion Desktop")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/mc-logo.svg')))
        self.setWindowState(QtCore.Qt.WindowMaximized)
        #self.setGeometry(1000, 0, 1000, 1000)

        self.mainPage = mainpage.MainPage(appStatus, dbConnection)
        self.setCentralWidget(self.mainPage)

        self.createMenu()
        self.createStatusBar()



    def createMenu(self):
        """ Menu:
        options [usertestmode, adaptivitymode, labellistorderadjustment)
        help    [about, shortcuts] """

        # OPTIONS
        optionsMenu = self.menuBar().addMenu("Options")

        self.userTestModeAction = QtWidgets.QAction('usertest mode', self, checkable=True, enabled=True)
        self.userTestModeAction.setStatusTip("when enabled the label lists expand as soon as timeline entry has focus")
        self.adaptivityModeAction = QtWidgets.QAction('adaptivity mode', self, checkable=True)
        self.adaptivityModeAction.setStatusTip("when enabled the system makes label suggestions based on the ml-algorithm")
        self.adjustLabelOrderAction = QtWidgets.QAction('adjust order of label lists', self, checkable=True)
        self.adjustLabelOrderAction.setStatusTip("when enabled the system adjusts the order in the label lists according to label suggestions")

        optionsMenu.addAction(self.userTestModeAction)
        optionsMenu.addAction(self.adaptivityModeAction)
        optionsMenu.addAction(self.adjustLabelOrderAction)

        # HELP
        helpMenu = self.menuBar().addMenu("Help")
        aboutAction = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/mc-logo.svg')),
            'About', self, triggered=self.aboutWindow)
        shortcutAction = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/Keyboard Filled-50.png')),
            'Shortcuts', self, triggered=self.shortcutWindow)

        aboutAction.setToolTip("get information about the Mobility Companion Desktop application")
        shortcutAction.setToolTip("show an overview of shortcuts to navigate the application")
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(shortcutAction)


    def aboutWindow(self):
        """ information about application displayed in separate window """
        self.aboutDialog = aboutwindow.AboutWindow()
        self.aboutDialog.show()


    def shortcutWindow(self):
        """ overview of usefull shortcuts """
        self.shortcutDialog = shortcutwindow.ShortcutWindow()
        self.shortcutDialog.show()


    def createStatusBar(self):
        """ StatusBar provides current status information like databaserange (and shortcut for last action used?) """
        self.myStatusBar = QtWidgets.QStatusBar()

        rangestring = 'database data ranges from '
        rangestring += QtCore.QDate(self.appStatus.databaseRange_utc[0]).toString(QtCore.Qt.DefaultLocaleShortDate)
        rangestring += ' to '
        rangestring += QtCore.QDate(self.appStatus.databaseRange_utc[1]).toString(QtCore.Qt.DefaultLocaleShortDate)
        databaserangeinfo = QtWidgets.QLabel(rangestring)
        self.myStatusBar.addPermanentWidget(databaserangeinfo)

        self.setStatusBar(self.myStatusBar)

        # TODO show progress: percentage labeled data