import os, sys
from PyQt5 import QtCore, QtWidgets, QtSvg
from gui.timelineview.labellists import labellists
from database import dbqueries
from helper import timehelper
from gui.style import iconfactory


class Timeline(QtWidgets.QListWidget):
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QListWidget.__init__(self)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        listHeight = 0

        entryList = appStatus.currentDateEntries

        for entry in entryList:
            listItem = QtWidgets.QListWidgetItem()
            # generate EntryWidget for each entry
            if entry['type'] == 'Stop':
                entryWidget = StopEntry(entry, dbConnection)
            elif entry['type'] == 'Movement':
                entryWidget = MovementEntry(entry, dbConnection)

            listItem.setSizeHint(entryWidget.sizeHint())
            self.addItem(listItem)
            self.setItemWidget(listItem, entryWidget)
            listHeight += listItem.sizeHint().height()

        self.setFixedHeight(listHeight)

        # TODO self.insertItem for movement split




class Entry(QtWidgets.QWidget):
    def __init__(self, time, icon, info, labelwidget):
        QtWidgets.QWidget.__init__(self)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.addSpacing(10)
        hlayout.addWidget(time, 0)
        hlayout.addWidget(icon, 0)
        hlayout.addStretch(1)
        info.setFixedWidth(130)
        hlayout.addWidget(info, 2)
        hlayout.addStretch(2)
        hlayout.addWidget(labelwidget, 2)
        hlayout.addStretch(7)
        #hlayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(hlayout)


class StopEntry(Entry):
    def __init__(self, stopentry, dbConnection):
        value = stopentry['value']
        time = EntryTime(value.startTime, value.endTime)

        stopicon = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/line.svg'))
        stopcircle = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/stop2.svg'), parent=stopicon)
        stopcircle.move(0, 32)

        address = dbqueries.getClusterNameForId(dbConnection, value.idCluster)
        address = address.split(', ')
        address = "\n".join(address)
        info = QtWidgets.QLabel(str(address))

        labelwidget = labellists.LabelWidget(stopentry['type'], value.placeTypeLabel, value.flagAutomaticLabeling, dbConnection)

        super(StopEntry, self).__init__(time,
                                        stopicon,
                                        info,
                                        labelwidget)


class MovementEntry(Entry):
    def __init__(self, movemententry, dbConnection):
        value = movemententry['value']

        time = EntryTime(value.originTime, value.destinationTime)
        movementicon = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), './res/line.svg'))

        distance, duration, velocity = dbqueries.getMovementAttributesForMovementId(dbConnection, value.id)
        info = MvmtAttributes(distance, duration, velocity)

        travelModeLabel = dbqueries.TravelModeForId(dbConnection, value.idType)
        labelwidget = labellists.LabelWidget(movemententry['type'], travelModeLabel, False, dbConnection)

        super(MovementEntry, self).__init__(time,
                                            movementicon,
                                            info,
                                            labelwidget)



class MvmtAttributes(QtWidgets.QWidget):
    def __init__(self, distance, duration, velocity):
        QtWidgets.QWidget.__init__(self)
        self.setFixedHeight(50)

        distance = QtWidgets.QLabel(str(distance))
        duration = QtWidgets.QLabel(str(duration))
        velocity = QtWidgets.QLabel(str(velocity))
        distanceIcon = iconfactory.DistanceIcon()
        durationIcon = iconfactory.ClockIcon()
        velocityIcon = iconfactory.SpeedometerIcon()
        distanceIcon.setFixedSize(15, 15)
        durationIcon.setFixedSize(15, 15)
        velocityIcon.setFixedSize(15, 15)

        gridlayout = QtWidgets.QGridLayout()
        gridlayout.setContentsMargins(0, 0, 0, 0)
        gridlayout.setVerticalSpacing(0)
        gridlayout.addWidget(distanceIcon, 0, 0)
        gridlayout.addWidget(distance, 0, 1)
        gridlayout.addWidget(durationIcon, 1, 0)
        gridlayout.addWidget(duration, 1, 1)
        gridlayout.addWidget(velocityIcon, 2, 0)
        gridlayout.addWidget(velocity, 2, 1)

        self.setLayout(gridlayout)




class EntryTime(QtWidgets.QWidget):
    def __init__(self, startTime, endTime):
        QtWidgets.QWidget.__init__(self)
        startTime = timehelper.timestamp_to_utc(startTime).time()
        endTime = timehelper.timestamp_to_utc(endTime).time()
        myformat = 'hh:mm'

        starttime = QtCore.QTime(startTime).toString(myformat)
        endtime = QtCore.QTime(endTime).toString(myformat)

        entrytime = QtWidgets.QLabel('<p style="line-height: 20px;">' + starttime + '<br>' + endtime + '</p>')

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(entrytime)
        self.setLayout(vlayout)

