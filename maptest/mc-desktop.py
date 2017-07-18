import os, sys
import logging
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuickWidgets

logger = logging.getLogger()


class MapView(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        mapspace = QtQuickWidgets.QQuickWidget()
        mapspace.setSource(QtCore.QUrl(os.path.join(os.path.dirname(__file__), 'mymap.qml')))
        mapspace.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)

        labelThatMakesItWork = QtWidgets.QLabel('test')
        # funktioniert auch, wenn das label height=0 hat
        #labelThatMakesItWork.setFixedHeight(0)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(mapspace)
        vlayout.addWidget(labelThatMakesItWork)        # wenn man diese Zeile aukommentiert kommt ein sigsegv - WHYYYY ???
        self.setLayout(vlayout)


class MainPage(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        # ------------------------------------------
        # calender und map zusammen gehen nur, wenn in dem map layout
        # noch das 'dummylabel' eingefügt wird.
        # ------------------------------------------
        left = QtWidgets.QTextEdit()
        cal = QtWidgets.QCalendarWidget()
        cal.setFixedWidth(500)
        mmap = MapView()

        # die map ganz ohne layout direkt einzusetzen funktioniert auch nicht
        # mmap = QtQuickWidgets.QQuickWidget()
        # mmap.setSource(QtCore.QUrl(os.path.join(os.path.dirname(__file__), 'mymap.qml')))
        # mmap.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(cal)
        hlayout.addWidget(mmap)
        self.setLayout(hlayout)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.setWindowTitle("MAP")
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.mainPage = MainPage()
        self.setCentralWidget(self.mainPage)


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)

        mainWindow = MainWindow()
        mainWindow.show()

        # Shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), mainWindow, app.quit)
        app.exec_()
        sys.exit(0)
    except SystemExit:
        logger.info("Closing Window...")
    except Exception as e:
        logger.error("Exception: {}".format(sys.exc_info()))