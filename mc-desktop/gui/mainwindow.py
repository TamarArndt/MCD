import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import mainpage
from gui.dialogs import pathconfigurationdialog, aboutwindow, shortcutwindow, settingswindow
from helper.filehelper import FileHelper


class MyTabWidget(QtWidgets.QTabWidget):
    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)

    def addClosableTab(self, newTabWidget, name):
        self.addTab(newTabWidget, name)
        tabBar = self.tabBar()
        closeButton = QtWidgets.QToolButton()
        closeButton.setStyleSheet(' QToolButton {border: none; background-color: transparent;} ')
        closeButton.setIcon(QtGui.QIcon(os.path.join(FileHelper().get_project_cwd(), 'res', 'ei-close.svg')))
        tabBar.setTabButton(self.count()-1, QtWidgets.QTabBar.RightSide, closeButton)

        closeButton.clicked.connect(lambda: print('trying to close tab'))
        #connect(tabBar(), SIGNAL(tabCloseRequested(int)), this, SLOT(deleteTab(int)));



class MainWindow(QtWidgets.QMainWindow):
    """ MainWindow encapsulates menu, statusbar and mainPage (containing calendar-, timeline- and mapview)"""
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.appStatus = appStatus

        # set Window
        self.setWindowTitle("Mobility Companion Desktop")
        self.setWindowIcon(QtGui.QIcon(os.path.join(FileHelper().get_project_cwd(), 'res', 'mc-logo.svg')))
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.mainPage = mainpage.MainPage(appStatus, dbConnection)

        self.tabWidget = MyTabWidget() #QtWidgets.QTabWidget()
        self.tabWidget.addTab(self.mainPage, 'Main Page')
        self.tabWidget.setTabBarAutoHide(True)
        #self.tabWidget.setTabsClosable(True)
        self.setCentralWidget(self.tabWidget)

        self.createMenu()
        self.createStatusBar()

    def createMenu(self):
        """ Menu:
        settings [path settings, adaptivitymode(on/off)]
        help    [about, shortcuts] """

        # SETTINGS
        settingsMenu = self.menuBar().addMenu("Settings")
        settingsMenu.setToolTipsVisible(True)

        # pathConfigurationAction = QtWidgets.QAction(
        #     'Filepath settings', self, triggered=self.pathConfigurationDialog)
        # pathConfigurationAction.setToolTip('Configure paths to database, .jar and .model file.')

        self.adaptivityModeAction = QtWidgets.QAction('Provide adaptive label suggestions', self, checkable=True, toggled=self.adaptivityModeSwitch)
        self.adaptivityModeAction.setChecked(self.appStatus.adaptivityMode)
        self.adaptivityModeAction.setStatusTip("see settings page for detailed information")
        self.adaptivityModeAction.setToolTip("see settings page for detailed information")
        # self.adaptivityModeAction.setStatusTip("When enabled the system will generate suggestions for labels based on the semantic place labeling algorithm.")
        # self.adaptivityModeAction.setToolTip("When enabled the system will generate suggestions for labels based on the semantic place labeling algorithm.")

        self.automaticLabelingModeAction = QtWidgets.QAction('Automatic labeling', self, checkable=True, toggled=self.automaticLabelingModeSwitch)
        self.automaticLabelingModeAction.setChecked(self.appStatus.automaticLabelingMode)
        self.automaticLabelingModeAction.setStatusTip("see settings page for detailed information")
        self.automaticLabelingModeAction.setToolTip("see settings page for detailed information")
        # self.automaticLabelingModeAction.setStatusTip("When enabled the system will memorize place type associations for places you visit.")
        # self.automaticLabelingModeAction.setToolTip("When enabled the system will memorize place type associations for places you visit.")

        settingsAction = QtWidgets.QAction('Settings page', self, triggered=self.showSettingsWindow)

        #settingsMenu.addAction(pathConfigurationAction)
        settingsMenu.addAction(settingsAction)
        settingsMenu.addAction(self.adaptivityModeAction)
        settingsMenu.addAction(self.automaticLabelingModeAction)

        # HELP
        helpMenu = self.menuBar().addMenu("About")
        aboutAction = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(FileHelper().get_project_cwd(), 'res', 'mc-logo.svg')),
            'About Mobility Companion', self, triggered=self.aboutWindow)
        shortcutAction = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(FileHelper().get_project_cwd(), 'res', 'Keyboard Filled-50.png')),
            'Keyboard Shortcuts Help', self, triggered=self.shortcutWindow)

        aboutAction.setToolTip("About the Mobility Companion Desktop application")
        shortcutAction.setToolTip("Get an overview of shortcuts for the application functions")
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(shortcutAction)

    def showSettingsWindow(self):
        """ insert settings tab if not already existent """
        # TODO check if settings Window should rather be renewed each time
        for index in range(self.tabWidget.count()):
            if self.tabWidget.tabText(index) == 'Settings':
                self.tabWidget.setCurrentIndex(index)
                return
        self.settingsWindow = settingswindow.SettingsWindow()
        self.tabWidget.addClosableTab(self.settingsWindow, 'Settings')
        self.tabWidget.setCurrentWidget(self.settingsWindow)
        #self.tabWidget.tabBar()

    #
    # def pathConfigurationDialog(self):
    #     self.pathConfigurationDialog = pathconfigurationdialog.PathConfigurationDialog()
    #     self.pathConfigurationDialog.show()

    def adaptivityModeSwitch(self):
        self.appStatus.adaptivityMode = self.adaptivityModeAction.isChecked()

    def automaticLabelingModeSwitch(self):
        self.appStatus.automaticLabelingMode = self.automaticLabelingModeAction.isChecked()

    def aboutWindow(self):
        """ information about application displayed in separate window """
        for index in range(self.tabWidget.count()):
            if self.tabWidget.tabText(index) == 'About':
                self.tabWidget.setCurrentIndex(index)
                return
        self.aboutDialog = aboutwindow.AboutWindow()
        self.tabWidget.addClosableTab(self.aboutDialog, 'About')
        self.tabWidget.setCurrentWidget(self.aboutDialog)


    def shortcutWindow(self):
        """ overview of usefull shortcuts """
        self.shortcutDialog = shortcutwindow.ShortcutWindow()
        self.shortcutDialog.show()

    def createStatusBar(self):
        """ StatusBar provides current status information like databaserange (and shortcut for last action used?) """
        self.myStatusBar = QtWidgets.QStatusBar()

        rangestring = 'database data ranges from '
        rangestring += QtCore.QDate(self.appStatus.databaseRange_timestring[0]).toString(QtCore.Qt.DefaultLocaleShortDate)
        rangestring += ' to '
        rangestring += QtCore.QDate(self.appStatus.databaseRange_timestring[1]).toString(QtCore.Qt.DefaultLocaleShortDate)
        databaserangeinfo = QtWidgets.QLabel(rangestring)
        self.myStatusBar.addPermanentWidget(databaserangeinfo)

        self.setStatusBar(self.myStatusBar)

        # TODO show progress: percentage labeled data