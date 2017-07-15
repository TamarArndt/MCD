import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from gui import mainpage
from gui.dialogs import pathconfigurationdialog, aboutwindow, shortcutwindow


class MainWindow(QtWidgets.QMainWindow):
    """ MainWindow encapsulates menu, statusbar and mainPage (containing calendar-, timeline- and mapview)"""
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.appStatus = appStatus

        # set Window
        self.setWindowTitle("Mobility Companion Desktop")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg')))
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.mainPage = mainpage.MainPage(appStatus, dbConnection)
        self.setCentralWidget(self.mainPage)

        self.createMenu()
        self.createStatusBar()

    def createMenu(self):
        """ Menu:
        settings [path settings, adaptivitymode(on/off)]
        help    [about, shortcuts] """

        # SETTINGS
        settingsMenu = self.menuBar().addMenu("Settings")
        settingsMenu.setToolTipsVisible(True)

        pathConfigurationAction = QtWidgets.QAction(
            'Filepath settings', self, triggered=self.pathConfigurationDialog)
        pathConfigurationAction.setToolTip('Configure paths to database, .jar and .model file.')

        self.adaptivityModeAction = QtWidgets.QAction('Provide adaptive label suggestions', self, checkable=True, toggled=self.adaptivityModeSwitch)
        self.adaptivityModeAction.setChecked(self.appStatus.adaptivityMode)
        self.adaptivityModeAction.setStatusTip("When enabled the system will generate suggestions for labels based on the semantic place labeling algorithm.")
        self.adaptivityModeAction.setToolTip("When enabled the system will generate suggestions for labels based on the semantic place labeling algorithm.")

        self.automaticLabelingModeAction = QtWidgets.QAction('Automatic labeling', self, checkable=True, toggled=self.automaticLabelingModeSwitch)
        self.automaticLabelingModeAction.setChecked(self.appStatus.automaticLabelingMode)
        self.automaticLabelingModeAction.setStatusTip("When enabled the system will memorize place type associations for places you visit.")
        self.automaticLabelingModeAction.setToolTip("When enabled the system will memorize place type associations for places you visit.")

        settingsMenu.addAction(pathConfigurationAction)
        settingsMenu.addAction(self.adaptivityModeAction)
        settingsMenu.addAction(self.automaticLabelingModeAction)

        # HELP
        helpMenu = self.menuBar().addMenu("About")
        aboutAction = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg')),
            'About', self, triggered=self.aboutWindow)
        shortcutAction = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'Keyboard Filled-50.png')),
            'Shortcuts', self, triggered=self.shortcutWindow)

        aboutAction.setToolTip("About the Mobility Companion Desktop application")
        shortcutAction.setToolTip("Get an overview of shortcuts for the application functions")
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(shortcutAction)

    def pathConfigurationDialog(self):
        self.pathConfigurationDialog = pathconfigurationdialog.PathConfigurationDialog()
        self.pathConfigurationDialog.show()

    def adaptivityModeSwitch(self):
        self.appStatus.adaptivityMode = self.adaptivityModeAction.isChecked()

    def automaticLabelingModeSwitch(self):
        self.appStatus.automaticLabelingMode = self.automaticLabelingModeAction.isChecked()

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