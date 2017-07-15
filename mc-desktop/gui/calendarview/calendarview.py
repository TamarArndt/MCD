import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.style import styleparser

class CalendarView(QtWidgets.QWidget):
    def __init__(self, appStatus):
        super(CalendarView, self).__init__()

        dbrange_utc = appStatus.databaseRange_utc
        self.calendar = MyCalendar(dbrange_utc)
        self.setFixedWidth(self.calendar.width() + 20)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(10, 6, 10, 0)
        vlayout.addWidget(self.calendar)
        vlayout.addStretch(1)
        self.setLayout(vlayout)


class MyCalendar(QtWidgets.QCalendarWidget):
    clickedOrActivated = QtCore.pyqtSignal(QtCore.QDate)
    def __init__(self, range):
        QtWidgets.QCalendarWidget.__init__(self)

        # bundle clicked and activated signal to one
        self.clicked[QtCore.QDate].connect(self.emitClickedOrActivatedSignal)
        self.activated[QtCore.QDate].connect(self.emitClickedOrActivatedSignal)
        # could use selectionChanged signal instead but this is emitted also when signal input comes from timelineHeader dateLabel
        # such that everything is updated twice when date in timelineHeader is changed

        self.range = range
        self.setSelectedDate(range[0])
        self.setMinimumDate(range[0])
        self.setMaximumDate(range[1])

        # style
        stylesheetFilename = 'calendarstylesheet.css'
        processedstylesheetPath = styleparser.preprocessStylesheet(stylesheetFilename)
        with open(processedstylesheetPath, 'r', encoding='utf-8') as file:
            processedstylesheet = file.read()
            self.setStyleSheet(processedstylesheet)

        self.setFixedHeight(210)
        self.setFixedWidth(240)
        # maybe set this relative to available screen, but needs to be fixed somehow.
        # see: desktop = QtWidgets.QDesktopWidget(), desktop.primaryScreen()), desktop.availableGeometry(self)

        #self.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.SingleLetterDayNames)
        self.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.setWeekdayTextFormat(QtCore.Qt.Saturday, QtGui.QTextCharFormat())
        self.setWeekdayTextFormat(QtCore.Qt.Sunday, QtGui.QTextCharFormat())
        header_format = QtGui.QTextCharFormat()
        header_format.setForeground(QtCore.Qt.darkGray)
        self.setHeaderTextFormat(header_format)

        # style calendar arrows (in a somewhat cumbersome way, but seems to be the only one)
        calendarNavBar = self.findChild(QtWidgets.QWidget, "qt_calendar_navigationbar")
        calendarNavBar.setObjectName('calendarNavBar')
        if calendarNavBar:
            nextMonth = calendarNavBar.findChild(QtWidgets.QWidget, "qt_calendar_nextmonth")
            prevMonth = calendarNavBar.findChild(QtWidgets.QWidget, "qt_calendar_prevmonth")
            monthButton = calendarNavBar.findChild(QtWidgets.QWidget, "qt_calendar_monthbutton")
            monthButton.setObjectName('monthButton')
            if nextMonth:
                nextMonth.setArrowType(QtCore.Qt.RightArrow)
            if prevMonth:
                prevMonth.setArrowType(QtCore.Qt.LeftArrow)

                #self.selectionChanged.connect(self.updateCells)

    def paintCell(self, painter, rect, date):
        """ overwrite paintCell method to change background for enabled range and to visualize labeling progress """
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)

        # style colors for database range: enabled range
        rangeformat = QtGui.QTextCharFormat()
        rangeformat.setBackground(QtCore.Qt.white)
        mycolor = QtGui.QColor.fromRgb(25, 118, 210) #primaryDarkColor
        rangeformat.setForeground(mycolor)
        otherformat = QtGui.QTextCharFormat()
        otherformat.setForeground(QtCore.Qt.lightGray)
        if date >= self.range[0] and date <= self.range[1]:
            self.setDateTextFormat(date, rangeformat)
        else:
            self.setDateTextFormat(date, otherformat)

        # TODO (maybe): Calendar visualize labelstate of date (color/symbol)
        singleformat = QtGui.QTextCharFormat()
        singleformat.setBackground(QtCore.Qt.yellow)
        if date == QtCore.QDate.currentDate():
            self.setDateTextFormat(date, singleformat)

            # <===> that fills with color
            # empty: not labeled
            # half full: partly labeled
            # full: fully labeled
            # no symbol at all: no detection

    def emitClickedOrActivatedSignal(self):
        self.clickedOrActivated.emit(self.selectedDate())