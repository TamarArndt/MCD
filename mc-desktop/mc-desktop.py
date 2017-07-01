import os, sys
import logging, traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import mainwindow
from appstatus import applicationstatus
from database import dbconnection

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig()


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        MAIN_DIR = os.path.dirname(sys.modules['__main__'].__file__)

        # initialize a dbConnection and an object that holds the applications' status information
        DB_PATH = os.path.join(MAIN_DIR, './assets/data.db')
        dbConnection = dbconnection.DatabaseConnection(DB_PATH)
        appStatus = applicationstatus.ApplicationStatus(dbConnection) # databaseRange, currentDate, currentDateEntries

        # set StyleSheet for whole application
        with open(os.path.join(MAIN_DIR , './gui/style/mainstylesheet.css'), 'r', encoding='utf-8') as file:
            stylesheet = file.read()
            app.setStyleSheet(stylesheet)

        mainWindow = mainwindow.MainWindow(appStatus, dbConnection)
        mainWindow.show()

        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), mainWindow, app.quit)
        app.exec_()
        sys.exit(0)
    except NameError:
        logger.error(" Name Error: {}".format(sys.exc_info()))
    except SystemExit:
        logger.info(" Closing Window...")
    except Exception as e:
        logger.error(" Exception: {}".format(sys.exc_info()))
        traceback.print_exc(file=sys.stdout)