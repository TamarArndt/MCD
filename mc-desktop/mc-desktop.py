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
        # --------------------------------------------------------------------------------
        # optional arguments on startup: only for usertest
        # --------------------------------------------------------------------------------
        parser = argparse.ArgumentParser()
        parser.add_argument('--usertestmode', help='enables usertest mode')
        parser.add_argument('--adaptivitymode', help='enables adaptive label suggestions generated with semantic place labeling algorithm, can also be changed from within the app')
        args = parser.parse_args()

        # set to True if argument is given
        if args.usertestmode:
            usertestMode = args.usertestmode  # True
        else:
            usertestMode = True #False
        if args.adaptivitymode:
            adaptivityMode = args.adaptivitymode  # True
        else:
            adaptivityMode = False

        logger.info("start programm | UsertestMode: %s | AdaptivityMode: %s", usertestMode, adaptivityMode )
        # --------------------------------------------------------------------------------
        # application
        # --------------------------------------------------------------------------------
        app = QtWidgets.QApplication(sys.argv)
        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        MAIN_DIR = os.path.dirname(sys.modules['__main__'].__file__)  # TODO MAIN_DIR not working on windows

        # set main stylesheet
        stylesheetFilename = 'mainstylesheet.css'
        processedstylesheetPath = styleparser.preprocessStylesheet(stylesheetFilename)
        with open(processedstylesheetPath, 'r', encoding='utf-8') as file:
            processedstylesheet = file.read()
            app.setStyleSheet(processedstylesheet)

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
        if not usertestMode:
            dbqueries.mergeConsecutiveMovementsWithSameTravelMode(dbConnection)
        appStatus = applicationstatus.ApplicationStatus(dbConnection, usertestMode, adaptivityMode)

        # --------------------------------------------------------------------------------
        # start main application window and welcome message
        # --------------------------------------------------------------------------------
        # optional welcome window
        if usertestMode:
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