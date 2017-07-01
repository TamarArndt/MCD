from PyQt5 import QtCore, QtGui, QtWidgets
from gui.calendarview import calendarview
from gui.timelineview import timelineview
from gui.mapview import mapview


class MainPage(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        super(MainPage, self).__init__()

        # components of MainPage
        self.calendar_view = calendarview.CalendarView(appStatus)
        self.timeline_view = timelineview.TimelineView(appStatus, dbConnection)
        self.map_view = mapview.MapView(appStatus, dbConnection)
        # TODO manage appStatus in MapView

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
        # - communicate datechange between calendar, timelineHeader, mapview and appStatus object
        # - inform map about selected entry in timeline

        self.communicateDateChange(appStatus, dbConnection)
        self.communicateSelectedTimelineEntryToMap()


    def communicateDateChange(self, appStatus, dbConnection):
        calendarinstance = self.calendar_view.calendar
        timelineheaderinstance = self.timeline_view.timelineHeader
        timelinecontent = self.timeline_view.timelineContent
        mapviewinstance = self.map_view

        # connect calendar to appStatus object, timelineHeader and tell timeline and mapview to update itself
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(lambda: appStatus.setCurrentDate(calendarinstance.selectedDate(), dbConnection))
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(timelineheaderinstance.dateLabel.updateDateLabel)
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(timelinecontent.updateTimelineContent)
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(mapviewinstance.showRouteOfCurrentDateOnMap) # shows route of whole day

        # connect timelineHeader to dbConnection object, calendar and tell timeline and mapview to update itself
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(lambda: appStatus.setCurrentDate(timelineheaderinstance.dateLabel.currentDate, dbConnection))
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(calendarinstance.setSelectedDate)
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(timelinecontent.updateTimelineContent)
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(mapviewinstance.showRouteOfCurrentDateOnMap)


    def communicateSelectedTimelineEntryToMap(self):
        timelineEntryListWidgetInstace = self.timeline_view.timelineContent.timeline
        mapviewinstance = self.map_view

        timelineEntryListWidgetInstace.currentRowChanged.connect(lambda: mapviewinstance.showSelectedEntryOnMap(timelineEntryListWidgetInstace.currentRow()))
