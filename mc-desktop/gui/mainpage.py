from PyQt5 import QtCore, QtGui, QtWidgets
from gui.calendarview import calendarview
from gui.timelineview import timelineview, waitingspinnerwidget
from gui.mapview import mapview
from database import dbupdates
from database.dbconnection import DatabaseConnection
from appstatus.applicationstatus import ApplicationStatus


class MainPage(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        super(MainPage, self).__init__()

        # components of MainPage
        self.calendar_view = calendarview.CalendarView(appStatus)
        self.map_view = mapview.MapView(appStatus, dbConnection, alwaysShowEntirePath=True)
        self.timeline_view = timelineview.TimelineView(appStatus, dbConnection, self.map_view)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self.calendar_view)
        splitter.addWidget(self.timeline_view)
        splitter.addWidget(self.map_view)
        splitter.setSizes([1, 400, 300])

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setSpacing(0)
        hlayout.addWidget(splitter)
        self.setLayout(hlayout)

        # Manage connections between components:
        # communicate datechange between calendar, timelineHeader, mapview and appStatus object
        self.communicateDateChange(appStatus, dbConnection)
        self.map_view.splitSignal[ApplicationStatus, DatabaseConnection, int, str].connect(self.actionsInCaseOfSplitEvent)

    def communicateDateChange(self, appStatus, dbConnection):
        calendarinstance = self.calendar_view.calendar
        timelineheaderinstance = self.timeline_view.timelineHeader
        timelinecontent = self.timeline_view.timelineContent
        mapviewinstance = self.map_view

        # connect calendar to appStatus object, timelineHeader and tell timeline and mapview to update themselves
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(lambda: appStatus.setCurrentDate(calendarinstance.selectedDate(), dbConnection))
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(timelineheaderinstance.dateLabel.updateDateLabel)
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(lambda: timelinecontent.updateTimelineContent(appStatus, dbConnection, mapviewinstance))
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(lambda: mapviewinstance.showRouteOfCurrentDateOnMap(appStatus))  # shows route of entire day

        # connect timelineHeader to dbConnection object, calendar and tell timeline and mapview to update themselves
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(lambda: appStatus.setCurrentDate(timelineheaderinstance.dateLabel.currentDate, dbConnection))
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(calendarinstance.setSelectedDate)
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(lambda: timelinecontent.updateTimelineContent(appStatus, dbConnection, mapviewinstance))
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(lambda: mapviewinstance.showRouteOfCurrentDateOnMap(appStatus))

    def actionsInCaseOfSplitEvent(self, appStatus, dbConnection, movementId, splittime):
        dbupdates.splitMovementAtTime(dbConnection, movementId=movementId, splittime=int(splittime))
        self.timeline_view.timelineContent.reevaluateTimelineContent(appStatus, dbConnection, self.map_view)