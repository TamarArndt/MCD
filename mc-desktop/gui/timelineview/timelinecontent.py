from PyQt5 import QtCore, QtGui, QtWidgets
from gui.timelineview import notification, timelineentrylist, questionnaire


class TimelineContent(QtWidgets.QWidget):
    loadingSignal = QtCore.pyqtSignal(bool)

    def __init__(self, appStatus, dbConnection, mapview):
        QtWidgets.QWidget.__init__(self)

        # components
        self.notification = notification.Notification(appStatus.labelingStatusForCurrentDate)
        self.timeline = timelineentrylist.Timeline(appStatus, dbConnection, mapview)
        self.questionnaire = questionnaire.Questionnaire(appStatus, dbConnection)

        if appStatus.labelingStatusForCurrentDate.totalNumberOfStops == 0:
            self.questionnaire.setHidden(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.notification)
        self.layout.setAlignment(self.notification, QtCore.Qt.AlignTop)
        self.layout.addWidget(self.timeline, 1)
        self.layout.setAlignment(self.timeline, QtCore.Qt.AlignTop)
        self.layout.addWidget(self.questionnaire, 1)
        self.setLayout(self.layout)

        self.timeline.numberOfLabeledEntriesChangedSignal.connect(lambda: self.updateNotification(appStatus))
        self.timeline.updateNecessary.connect(lambda: self.reevaluateTimelineContent(appStatus, dbConnection, mapview))

    def updateTimelineContent(self, appStatus, dbConnection, mapview):
        #self.loadingSignal.emit(True)
        # update components
        self.updateNotification(appStatus)
        newtimeline = timelineentrylist.Timeline(appStatus, dbConnection, mapview)
        newquestionnaire = questionnaire.Questionnaire(appStatus, dbConnection)

        self.updateTimeline(newtimeline)
        self.updateQuestionnaire(newquestionnaire)

        if appStatus.labelingStatusForCurrentDate.totalNumberOfStops == 0:
            self.questionnaire.setHidden(True)

        self.timeline.numberOfLabeledEntriesChangedSignal.connect(lambda: self.updateNotification(appStatus))
        #self.loadingSignal.emit(False)


    def updateNotification(self, appStatus):
        self.notification.setContent(appStatus.labelingStatusForCurrentDate)

    def updateTimeline(self, newtimeline):
        self.layout.removeWidget(self.timeline)
        self.timeline.setParent(None)
        self.timeline = newtimeline
        self.layout.insertWidget(1, self.timeline, 1)
        self.layout.setAlignment(self.timeline, QtCore.Qt.AlignTop)

    def updateQuestionnaire(self, newquestionnaire):
        self.layout.removeWidget(self.questionnaire)
        self.questionnaire.setParent(None)
        self.questionnaire = newquestionnaire
        self.layout.insertWidget(2, self.questionnaire, 1)

    def reevaluateTimelineContent(self, appStatus, dbConnection, mapview):
        row = self.timeline.currentRow()
        appStatus.updateApplicationStatus(dbConnection)
        self.updateTimelineContent(appStatus, dbConnection, mapview)
        self.timeline.setCurrentRow(row)



