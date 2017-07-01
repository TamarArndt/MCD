from PyQt5 import QtCore, QtGui, QtWidgets
from gui.timelineview import notification, timelineentrylist, questionnaire

class TimelineContent(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QWidget.__init__(self)
        #self.appStatus = appStatus

        # components
        self.notification = notification.Notification()
        self.timeline = timelineentrylist.Timeline(appStatus, dbConnection)
        self.questionnaire = questionnaire.Questionnaire()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.notification, 1)
        self.layout.addWidget(self.timeline, 3)
        self.layout.addWidget(self.questionnaire, 3)
        self.setLayout(self.layout)

    def updateTimelineContent(self):
        print('update Timeline Content')


    def updateNotification(self, status):
        # je nach status auf notification die entsprechende Funktion aufrufen
        pass

    def updateTimeline(self, timeline):
        self.layout.removeWidget(self.timeline)
        self.timeline.setParent(None)
        self.timeline = timeline
        self.layout.insertWidget(1, self.timeline)

    def updateQuestionnaire(self, questionnaire):
        self.layout.removeWidget(self.questionnaire)
        self.questionnaire.setParent(None)
        self.questionnaire = questionnaire
        self.layout.insertWidget(0, self.questionnaire)


