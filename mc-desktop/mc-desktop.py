import argparse
import os, sys
import logging.config
import logging, traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import mainwindow
from appstatus import applicationstatus
from database import dbconnection, dbqueries
import configuration.configuration as conf
from gui.dialogs import dbpathconfigurationonstartupdialog, welcomewindow
from gui.style import styleparser

logging.config.fileConfig("loggingconfiguration.ini")
logger = logging.getLogger()


if __name__ == '__main__':
    try:
        adaptivityMode = False

        logger.info("starting programm | AdaptivityMode: %s", adaptivityMode )
        # --------------------------------------------------------------------------------
        # application
        # --------------------------------------------------------------------------------
        app = QtWidgets.QApplication(sys.argv)
        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))

        # set main stylesheet
        stylesheetFilename = 'mainstylesheet.css'
        styleparser.StylesheetParser().setProcessedStyleSheet(stylesheetFilename, app)

        # --------------------------------------------------------------------------------
        # path configuration
        # --------------------------------------------------------------------------------
        # read current default values from configuration.ini
        DB_PATH, JAR_PATH, MODEL_PATH = conf.accessConfig()

        # database path configuration dialog on startup
        dbPathConfigurationDialog = dbpathconfigurationonstartupdialog.DatabasePathConfig(DB_PATH)
        if dbPathConfigurationDialog.exec() == QtWidgets.QDialog.Rejected:
           sys.exit(0)
        # update configuration.ini if default db path changed
        if not DB_PATH == dbPathConfigurationDialog.db_path:
           DB_PATH = dbPathConfigurationDialog.db_path

        # --------------------------------------------------------------------------------
        # initalize a database connection
        # set up application status object
        # --------------------------------------------------------------------------------
        dbConnection = dbconnection.DatabaseConnection(DB_PATH)
        dbqueries.mergeConsecutiveMovementsWithSameTravelMode(dbConnection)
        appStatus = applicationstatus.ApplicationStatus(dbConnection, adaptivityMode)

        # --------------------------------------------------------------------------------
        # start main application window
        # --------------------------------------------------------------------------------
        welcome = welcomewindow.WelcomeDialog(appStatus)
        welcome.show()

        mainWindow = mainwindow.MainWindow(appStatus, dbConnection)
        mainWindow.show()

        # Shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), mainWindow, app.quit)
        calendarShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Alt+c"), mainWindow)
        calendarShortcut.activated.connect(mainWindow.mainPage.calendar_view.calendar.setFocus)

        app.exec_()
        sys.exit(0)
    except NameError:
        logger.error("Name Error: {}".format(sys.exc_info()))
    except SystemExit:
        logger.info("Closing Window...")
    except Exception as e:
        logger.error("Exception: {}".format(sys.exc_info()))
        traceback.print_exc(file=sys.stdout)