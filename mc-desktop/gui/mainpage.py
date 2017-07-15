from PyQt5 import QtCore, QtGui, QtWidgets
from gui.calendarview import calendarview
from gui.timelineview import timelineview, waitingspinnerwidget
from gui.mapview import mapview, mapwidget
from database import dbupdates


class MainPage(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        super(MainPage, self).__init__()

        # TODO where does MapWidget Sigsegv come from?
        # x = QtWidgets.QWidget()
        # lay = QtWidgets.QVBoxLayout()
        # lay.setContentsMargins(0, 0, 0, 0)
        # lay.setSpacing(0)
        # lay.addWidget(mapwidget.MapWidget(), 1)
        # x.setLayout(lay)
        # #self.map_view = mapwidget.MapWidget()
        # #self.map_view = x


        # components of MainPage
        self.calendar_view = calendarview.CalendarView(appStatus)
        self.map_view = mapview.MapView(appStatus, dbConnection)
        self.timeline_view = timelineview.TimelineView(appStatus, dbConnection, self.map_view)

        self.waitingSpinner = waitingspinnerwidget.QtWaitingSpinner(parent=self.calendar_view)
        self.waitingSpinner.start()
        self.timeline_view.timelineContent.loadingSignal[bool].connect(self.controlWaitingSpinner)


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
        self.communicateDateChange(appStatus, dbConnection)

        self.map_view.splitSignal.connect(lambda: self.actionsInCaseOfSplitEvent(appStatus, dbConnection))


        #self.installEventFilter(self) #MyEventFilter())
        #self.calendar_view.calendar.installEventFilter(self)
        #self.timeline_view.timelineContent.timeline.installEventFilter(self)
        #self.calendar_view.installEventFilter(self)

        #print(self.calendar_view.calendar.children())
        # for obj in self.children():
        #     obj.installEventFilter(self)



    def communicateDateChange(self, appStatus, dbConnection):
        calendarinstance = self.calendar_view.calendar
        timelineheaderinstance = self.timeline_view.timelineHeader
        timelinecontent = self.timeline_view.timelineContent
        mapviewinstance = self.map_view

        # connect calendar to appStatus object, timelineHeader and tell timeline and mapview to update itself
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(lambda: appStatus.setCurrentDate(calendarinstance.selectedDate(), dbConnection))
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(timelineheaderinstance.dateLabel.updateDateLabel)
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(lambda: timelinecontent.updateTimelineContent(appStatus, dbConnection, mapviewinstance))
        calendarinstance.clickedOrActivated[QtCore.QDate].connect(lambda: mapviewinstance.showRouteOfCurrentDateOnMap(appStatus)) # shows route of whole day

        # connect timelineHeader to dbConnection object, calendar and tell timeline and mapview to update itself
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(lambda: appStatus.setCurrentDate(timelineheaderinstance.dateLabel.currentDate, dbConnection))
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(calendarinstance.setSelectedDate)
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(lambda: timelinecontent.updateTimelineContent(appStatus, dbConnection, mapviewinstance))
        timelineheaderinstance.dateLabel.speak[QtCore.QDate].connect(lambda: mapviewinstance.showRouteOfCurrentDateOnMap(appStatus))


    def actionsInCaseOfSplitEvent(self, appStatus, dbConnection):
        row = self.timeline_view.timelineContent.timeline.currentRow()
        dbupdates.splitMovementAtTime(dbConnection, movementId=self.map_view.split.movementId, splittime=self.map_view.split.currentTimestamp)

        appStatus.updateApplicationStatus(dbConnection)
        self.timeline_view.timelineContent.updateTimelineContent(appStatus, dbConnection, self.map_view)
        self.timeline_view.timelineContent.timeline.setCurrentRow(row)

    def controlWaitingSpinner(self, bool):
        self.waitingSpinner = waitingspinnerwidget.QtWaitingSpinner(parent=self.calendar_view)
        #print(bool)
        #self.waitingSpinner.stop()
        if bool:
            #print('starting')
            self.waitingSpinner.start()
        else:
            #print('stopping')
            self.waitingSpinner.stop()



    # -------------------------------------------------------------------------
    # KeyEvent management
    # -------------------------------------------------------------------------
    def eventFilter(self, targetObject, event):

        mCalendar = self.calendar_view.calendar
        mTimeline = self.timeline_view.timelineContent.timeline

        # if event.type() == QtCore.QEvent.ChildAdded:
        #     childEvent = QtCore.QChildEvent(event)
        #     childEvent.child().installEventFilter(self)
        #     print('child added', childEvent.child())
        #     pass

        if event.type() == QtCore.QEvent.MouseButtonPress:
            print('mouse button pressed')
        #if event.type() == QtCore.QEvent.MouseButtonPress:
        #    print(event, targetObject)

        #if not event.type() == QtGui.QPaintEvent:
            #print(targetObject, ' : ', event, ' : ', event.type())
        #from eventloggingusertest import eventlogging


        #mCalendar.installEventFilter(self)
        #mTimeline.installEventFilter(self)

        #if event.type() == QtCore.QEvent.MouseButtonPress:
        #    print('mouse event')
        #
        # if targetObject == mCalendar:
        #     print('mCalendar got event')
        #     if type(event) == QtCore.QEvent.MouseButtonPress:
        #         print('and it was a mouse button press')
        #         # cast ? QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);
        #         mouseEvent = QtGui.QMouseEvent(event)
        #         currentTime = QtCore.QDateTime.currentDateTime()
        #         eventlogging.logMousePress(targetObject, currentTime)

        return False #targetObject.eventFilter(targetObject, event)

        # eventFilter:
        # preprocess the events you are interested in
        # return False (dont actually filter anything out)

