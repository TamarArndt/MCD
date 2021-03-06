from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from gui.timelineview import timelineheader, timelinecontent, waitingspinnerwidget
from gui.style import styleparser

'''
The TimelineView is composed of:
+ TimelineHeader [shows the currently active date, has buttons for clicking through dates (prev, next)]
+ TimelineContent (Scrollarea), that capsules:
  + Notification [message about status of currently active date]
  + Timeline
  + Questionnaire
'''


class TimelineView(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection, mapview):
        QtWidgets.QWidget.__init__(self)

        stylesheetFilename = 'timelinestylesheet.css'
        styleparser.StylesheetParser().setProcessedStyleSheet(stylesheetFilename, self)

        self.timelineHeader = timelineheader.TimelineHeader(appStatus)
        self.timelineContent = timelinecontent.TimelineContent(appStatus, dbConnection, mapview)
        # self.setMinimumWidth(self.timelineContent.timeline.widthHint)

        # self.waitingSpinner = waitingspinnerwidget.QtWaitingSpinner(parent=self.timelineHeader)
        # self.waitingSpinner.start()
        # #self.timelineContent.loadingSignal[bool].connect(self.controlWaitingSpinner)

        scrollarea = QtWidgets.QScrollArea()
        scrollarea.setWidget(self.timelineContent)
        scrollarea.setWidgetResizable(True)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(self.timelineHeader)
        vlayout.addWidget(scrollarea)
        self.setLayout(vlayout)

    # def controlWaitingSpinner(self, bool):
    #     if bool:
    #         print('starting')
    #         self.waitingSpinner.start()
    #     else:
    #         print('stopping')
    #         self.waitingSpinner.stop()
    #


