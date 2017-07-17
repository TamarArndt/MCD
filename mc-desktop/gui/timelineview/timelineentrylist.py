import os, sys
import logging
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from gui.timelineview.labellists import labellists
from database import dbqueries, dbupdates
from helper import timehelper
from gui.style import iconfactory


class Timeline(QtWidgets.QListWidget):
    numberOfLabeledEntriesChangedSignal = QtCore.pyqtSignal()
    def __init__(self, appStatus, dbConnection, mapview):
        QtWidgets.QListWidget.__init__(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.listHeight = 0

        entryList = appStatus.currentDateEntries
        for index, entry in enumerate(entryList):
            listItem = MyListWidgetItem()

            # generate EntryWidget for each entry
            if entry['type'] == 'Stop':
                entryWidget = StopEntry(entry, dbConnection, appStatus, listItem)
            elif entry['type'] == 'Movement':
                entryWidget = MovementEntry(entry, dbConnection, appStatus, listItem)

            listItem.indexInEntryList = index
            listItem.entryWidget = entryWidget
            listItem.setSizeHint(entryWidget.sizeHint())
            self.addItem(listItem)
            self.setItemWidget(listItem, entryWidget)
            self.listHeight += listItem.sizeHint().height()

        self.setFixedHeight(self.listHeight)

        # connections
        self.currentRowChanged.connect(self.setFocusToCorrespondingLabelList)
        self.currentRowChanged.connect(lambda: mapview.showSelectedEntryOnMap(appStatus, self.currentItem().indexInEntryList))

    def setFocusToCorrespondingLabelList(self):
        logging.info(("selected entry: {}").format(self.currentItem().indexInEntryList))
        correspondingLabelList = self.currentItem().entryWidget.labelwidget.combobox
        correspondingLabelList.setFocus()

    def insertAutoLabelQuestion(self, index, dbConnection, stopId, selectedLabel):
        autoLabelQuestion = AutomaticLabelingQuestion(dbConnection, stopId, selectedLabel)
        listItem = QtWidgets.QListWidgetItem()
        listItem.setFlags(listItem.flags() & ~QtCore.Qt.ItemIsSelectable & ~QtCore.Qt.ItemIsEnabled)
        listItem.setSizeHint(autoLabelQuestion.sizeHint())
        self.insertItem(index, listItem)
        self.setItemWidget(listItem, autoLabelQuestion)
        self.listHeight += listItem.sizeHint().height()
        self.setFixedHeight(self.listHeight)
        autoLabelQuestion.finished.connect(lambda: self.removeAutoLabelQuestion(listItem, index))

    def removeAutoLabelQuestion(self, listItem, index):
        self.listHeight -= listItem.sizeHint().height()
        self.removeItemWidget(listItem)
        self.takeItem(index)
        self.setFixedHeight(self.listHeight)


class MyListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self):
        QtWidgets.QListWidgetItem.__init__(self)
        self.entryWidget = None
        self.indexInEntryList = None


class Entry(QtWidgets.QFrame):
    def __init__(self, time, icon, info, labelwidget, type): #info, labelwidget, type):
        QtWidgets.QFrame.__init__(self)

        self.setProperty('type', type)

        self.labelwidget = labelwidget #contentwidget.labelwidget
        self.selectionMarker = QtWidgets.QFrame()
        self.selectionMarker.setObjectName('selectionMarker')
        self.selectionMarker.setFixedWidth(13)
        #self.selectionMarker.setStyleSheet('QFrame {background-color: blue;}')

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        #hlayout.addSpacing(10)
        time.setFixedWidth(48)
        hlayout.addWidget(self.selectionMarker, 0)
        hlayout.addWidget(time, 0)
        hlayout.addWidget(icon, 0)

        info.setFixedWidth(140)
            # if type == 'Movement':
            #     pass
            #     #hlayout.addSpacing(20)
            #     #info.setFixedWidth(110)
            # #hlayout.addStretch(1)
        hlayout.addWidget(info, 2)
        hlayout.addStretch(2)
        hlayout.addWidget(labelwidget, 2)
        hlayout.addStretch(7)
        #hlayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        #hlayout.addWidget(contentwidget, 1)
        #hlayout.setAlignment(contentwidget, QtCore.Qt.AlignLeft)
        self.setLayout(hlayout)


class StopEntry(Entry):
    def __init__(self, stopentry, dbConnection, appStatus, correspondingListItem):
        value = stopentry['value']
        time = EntryTime(value.startTime, value.endTime)

        stopicon = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'line.svg'))
        stopcircle = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'stop.svg'), parent=stopicon)
        stopcircle.move(0, 32)

        addressCommaSeparated = dbqueries.getClusterNameForId(dbConnection, value.idCluster)
        address = addressCommaSeparated.split(', ')
        address = "<br/>".join(address)
        info = QtWidgets.QLabel(str(address))
        # TODO ?? xxx
        info.setWordWrap(True)
        #info = QtWidgets.QLabel('<strong>' + str(address) + '</strong>')
        info.setFixedWidth(140)

        isConfirmed = value.flagAutomaticLabeling == 2 or value.flagAutomaticLabeling == 3
        if appStatus.usertestMode:
            labelwidget = labellists.StopLabelWidgetUsertestMode(value.id, value.placeTypeLabel,
                                                                 isConfirmed, value.flagAutomaticLabeling,
                                                                 dbConnection, appStatus,
                                                                 correspondingListItem, addressCommaSeparated)

        else:
            labelwidget = labellists.StopLabelWidget(value.id, value.placeTypeLabel,
                                                     isConfirmed, value.flagAutomaticLabeling,
                                                     dbConnection, appStatus,
                                                     correspondingListItem, addressCommaSeparated)

        #stopContent = StopContent(info, labelwidget)

        super(StopEntry, self).__init__(time,
                                        stopicon,
                                        info, labelwidget,
                                        #StopContent(info, labelwidget),
                                        'Stop')


class MovementEntry(Entry):
    def __init__(self, movemententry, dbConnection, appStatus, correspondingListItem):
        value = movemententry['value']
        startTime, endTime, distance, duration, velocity = dbqueries.getMovementAttributesForMovementId(dbConnection, appStatus, value.id)

        time = QtWidgets.QWidget() #EntryTime(startTime, endTime)
        movementicon = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'line.svg'))

        info = MvmtAttributes(distance, duration, velocity)
        info.setFixedWidth(140)

        movementId = value.id
        travelModeLabel = dbqueries.TravelModeForId(dbConnection, value.idType)
        isConfirmed = not value.idType == 13  # 13: unknown
        labelwidget = labellists.MovementLabelWidget(movementId, travelModeLabel, isConfirmed,
                                                     dbConnection, appStatus, correspondingListItem)

        #movementContent = MovementContent(info, labelwidget)

        super(MovementEntry, self).__init__(time,
                                            movementicon,
                                            info, labelwidget,
                                            #MovementContent(info, labelwidget),
                                            'Movement')


class MvmtAttributes(QtWidgets.QWidget):
    def __init__(self, distance, duration, velocity):
        QtWidgets.QWidget.__init__(self)
        self.setFixedHeight(50)

        distance = QtWidgets.QLabel(str(distance) + ' km')
        duration = QtWidgets.QLabel(str(duration))
        velocity = QtWidgets.QLabel(str(velocity) + ' km/h')
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

# -----------------------------------------------------------
# content classes not in use
class StopContent(QtWidgets.QFrame):
    def __init__(self, address, stoplabelwidget):
        QtWidgets.QFrame.__init__(self)
        self.labelwidget = stoplabelwidget

        self.setStyleSheet('QFrame {background-color: white; border: 1px solid darkgray; border-radius: 3px;}')
        self.setFixedWidth(700)

        hlayout = QtWidgets.QHBoxLayout()

        hlayout.addWidget(address)
        hlayout.addWidget(stoplabelwidget)
        self.setLayout(hlayout)

class MovementContent(QtWidgets.QFrame):
    def __init__(self, attributes, movementlabelwidget):
        QtWidgets.QFrame.__init__(self)
        self.labelwidget = movementlabelwidget

        #self.setStyleSheet('QFrame {background-color: blue;}')

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(attributes)
        hlayout.addWidget(movementlabelwidget)
        self.setLayout(hlayout)
# -----------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------

class AutomaticLabelingQuestion(QtWidgets.QFrame):
    finished = QtCore.pyqtSignal()
    def __init__(self, dbConnection, stopId, selectedLabel):
        QtWidgets.QFrame.__init__(self)
        self.setObjectName('automaticLabelingQuestion')
        self.setToolTip("If you don't want to be asked this question again, disable automatic labeling in the settings menu.")

        question = QtWidgets.QLabel('Apply label "' + str(selectedLabel) + '" to all other unlabeled stops at this location?')
        question.setWordWrap(True)
        question.setObjectName('importantLabel')
        nobutton = QtWidgets.QPushButton('No')
        nobutton.setObjectName('smallButton')
        nobutton.setFixedWidth(nobutton.sizeHint().width())
        nobutton.clicked.connect(lambda: self.finished.emit())
        yesbutton = QtWidgets.QPushButton('Yes')
        yesbutton.setObjectName('smallButton')
        yesbutton.setFixedWidth(yesbutton.sizeHint().width())
        yesbutton.clicked.connect(lambda: self.accept(dbConnection, stopId, selectedLabel))

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addSpacing(2)
        hlayout.addWidget(question)
        hlayout.addWidget(nobutton)
        hlayout.addSpacing(2)
        hlayout.addWidget(yesbutton)
        hlayout.addSpacing(2)
        self.setLayout(hlayout)

    def accept(self, dbConnection, stopId, selectedLabel):
        dbupdates.newClusterPlaceTypeAssociation(dbConnection, stopId, selectedLabel)
        self.finished.emit()