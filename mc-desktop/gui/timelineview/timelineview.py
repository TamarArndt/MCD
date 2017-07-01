import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from gui.timelineview import timelineheader, timelinecontent

'''
The TimelineView is composed of:
+ TimelineHeader [shows the currently active date, has buttons for clicking through dates (prev, next)]
+ TimelineContent (Scrollarea), that capsules:
  + Notification [message about status of currently active date]
  + Timeline
  + Questionnaire
'''


class TimelineView(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QWidget.__init__(self)

        with open(os.path.join(os.path.dirname(sys.modules['__main__'].__file__) , './gui/style/timelinestylesheet.css'), 'r', encoding='utf-8') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

        self.timelineHeader = timelineheader.TimelineHeader(appStatus)
        self.timelineContent = timelinecontent.TimelineContent(appStatus, dbConnection)

        scrollarea = QtWidgets.QScrollArea()
        scrollarea.setWidget(self.timelineContent)
        scrollarea.setWidgetResizable(True)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(self.timelineHeader)
        vlayout.addWidget(scrollarea)
        self.setLayout(vlayout)



