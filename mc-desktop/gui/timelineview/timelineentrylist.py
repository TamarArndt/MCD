import os, sys
import logging
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from gui.timelineview.labellists import labellists
from database import dbqueries, dbupdates
from helper import timehelper
from gui.style import iconfactory
from helper.filehelper import FileHelper

class Timeline(QtWidgets.QListWidget):
    numberOfLabeledEntriesChangedSignal = QtCore.pyqtSignal()
    updateNecessary = QtCore.pyqtSignal()
    
    def __init__(self, appStatus, dbConnection, mapview):
        QtWidgets.QListWidget.__init__(self)
        #self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.listHeight = 0
        widths = [0]

        entryList = appStatus.currentDateEntries
        for index, entry in enumerate(entryList):
            listItem = MyListWidgetItem()

            # generate EntryWidget for each entry
            if entry['type'] == 'Stop':
                entryWidget = StopEntry(entry, dbConnection, appStatus, listItem)
                listItem.setBackground(QtGui.QColor(220, 220, 220)) #218, 222, 230))
            elif entry['type'] == 'Movement':
                entryWidget = MovementEntry(entry, dbConnection, appStatus, listItem)
                listItem.setBackground(QtGui.QColor(245, 245, 245))

            listItem.indexInEntryList = index
            listItem.entryWidget = entryWidget
            listItem.setSizeHint(entryWidget.sizeHint())
            self.addItem(listItem)
            self.setItemWidget(listItem, entryWidget)
            self.listHeight += listItem.sizeHint().height()
            widths.append(listItem.sizeHint().width())

        self.widthHint = max(widths)
        self.setFixedHeight(self.listHeight)


        # connections
        self.currentRowChanged.connect(self.setFocusToCorrespondingLabelList)
        self.currentRowChanged.connect(lambda: mapview.showSelectedEntryOnMap(appStatus, self.currentItem().indexInEntryList, False))
        self.itemDoubleClicked.connect(lambda: mapview.showSelectedEntryOnMap(appStatus, self.currentItem().indexInEntryList, True))

    def setFocusToCorrespondingLabelList(self):
        #logging.info(("selected entry: {}").format(self.currentItem().indexInEntryList))
        correspondingLabelList = self.currentItem().entryWidget.labelwidget.combobox
        correspondingLabelList.setFocus()

    def insertAutoLabelQuestion(self, index, dbConnection, stopId, selectedLabel):
        if type(self.item(index)) == AutomaticLabelingQuestionListWidgetItem:
            self.removeAutoLabelQuestion(self.item(index), index)
        autoLabelQuestionItem = AutomaticLabelingQuestionListWidgetItem(dbConnection, stopId, selectedLabel)
        autoLabelQuestion = autoLabelQuestionItem.autoLabelQuestion
        self.insertItem(index, autoLabelQuestionItem)
        self.setItemWidget(autoLabelQuestionItem, autoLabelQuestion)
        self.listHeight += autoLabelQuestionItem.sizeHint().height()
        self.setFixedHeight(self.listHeight)
        autoLabelQuestion.accepted.connect(lambda: self.removeAutoLabelQuestion(autoLabelQuestionItem, index, True))
        autoLabelQuestion.rejected.connect(lambda: self.removeAutoLabelQuestion(autoLabelQuestionItem, index, False))

    def removeAutoLabelQuestion(self, listItem, index, updateNecessary):
        self.listHeight -= listItem.sizeHint().height()
        self.removeItemWidget(listItem)
        self.takeItem(index)
        self.setFixedHeight(self.listHeight)
        if updateNecessary:
            pass
            #self.updateNecessary.emit()


class MyListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self):
        QtWidgets.QListWidgetItem.__init__(self)
        self.entryWidget = None
        self.indexInEntryList = None

class AutomaticLabelingQuestionListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, dbConnection, stopId, selectedLabel):
        QtWidgets.QListWidgetItem.__init__(self)
        self.autoLabelQuestion = AutomaticLabelingQuestion(dbConnection, stopId, selectedLabel)
        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsSelectable & ~QtCore.Qt.ItemIsEnabled)
        self.setSizeHint(self.autoLabelQuestion.sizeHint())


class Entry(QtWidgets.QFrame):
    def __init__(self, time, icon, info, labelwidget, type):
        QtWidgets.QFrame.__init__(self)

        self.setProperty('type', type)
        self.labelwidget = labelwidget

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(10, 0, 10, 0)
        time.setFixedWidth(48)
        hlayout.addWidget(time, 0)
        icon.setFixedWidth(icon.sizeHint().width())
        hlayout.addWidget(icon, 0)
        hlayout.addSpacing(10)

        maxsizeestimater = QtWidgets.QLabel('Auf der Morgenstelle 28')
        info.setFixedWidth(maxsizeestimater.sizeHint().width()+15)
        hlayout.addWidget(info, 2)
        hlayout.addSpacing(10)
        hlayout.addWidget(labelwidget, 2)
        hlayout.setAlignment(labelwidget, QtCore.Qt.AlignCenter)
        #hlayout.addStretch(1)
        self.setLayout(hlayout)


class StopEntry(Entry):
    def __init__(self, stopentry, dbConnection, appStatus, correspondingListItem):
        value = stopentry['value']
        time = EntryTime(value.startTime, value.endTime)
        PROJECT_DIR = FileHelper().get_project_cwd()

        stopicon = QtSvg.QSvgWidget(os.path.join(PROJECT_DIR, 'res', 'icon_mvmt.svg'))
        stopcircle = QtSvg.QSvgWidget(os.path.join(PROJECT_DIR, 'res', 'icon_stop.svg'), parent=stopicon)
        stopcircle.move(0,5)

        addressCommaSeparated = dbqueries.getClusterNameForId(dbConnection, value.idCluster)
        address = addressCommaSeparated.split(', ')
        address = "<br/>".join(address)
        info = QtWidgets.QLabel(str(address))
        info.setWordWrap(True)

        isConfirmed = value.flagAutomaticLabeling == 2 or value.flagAutomaticLabeling == 3

        labelwidget = labellists.StopLabelWidget(value.id, value.placeTypeLabel,
                                                 isConfirmed, value.flagAutomaticLabeling,
                                                 dbConnection, appStatus,
                                                 correspondingListItem, addressCommaSeparated)

        super(StopEntry, self).__init__(time,
                                        stopicon,
                                        info, labelwidget,
                                        'Stop')


class MovementEntry(Entry):
    def __init__(self, movemententry, dbConnection, appStatus, correspondingListItem):
        PROJECT_DIR = FileHelper().get_project_cwd()
        value = movemententry['value']
        startTime, endTime, distance, duration, velocity = dbqueries.getMovementAttributesForMovementId(dbConnection, appStatus, value.id)

        time = QtWidgets.QWidget()
        movementicon = QtSvg.QSvgWidget(os.path.join(PROJECT_DIR, 'res', 'icon_mvmt.svg'))

        info = MvmtAttributes(distance, duration, velocity)
        movementId = value.id
        travelModeLabel = dbqueries.TravelModeForId(dbConnection, value.idType)
        isConfirmed = not value.idType == 13  # 13: unknown
        labelwidget = labellists.MovementLabelWidget(movementId, travelModeLabel, isConfirmed,
                                                     dbConnection, appStatus, correspondingListItem)

        super(MovementEntry, self).__init__(time,
                                            movementicon,
                                            info, labelwidget,
                                            'Movement')
# TODO
class ShortStopEntry(Entry):
    def __init__(self, shortstopentry, dbConnection, appStatus, correspondingListItem):
        pass

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


# ------------------------------------------------------------------------------------------------------------------

class AutomaticLabelingQuestion(QtWidgets.QFrame):
    #finished = QtCore.pyqtSignal()
    accepted = QtCore.pyqtSignal()
    rejected = QtCore.pyqtSignal()
    def __init__(self, dbConnection, stopId, selectedLabel):
        QtWidgets.QFrame.__init__(self)
        self.setObjectName('automaticLabelingQuestion')
        self.setToolTip("If you don't want to be asked this question again, disable automatic labeling in the settings menu.")

        indicator = QtWidgets.QFrame()
        indicator.setStyleSheet('QFrame {background-color: #507EB1;}')
        indicator.setFixedWidth(10)
        question = QtWidgets.QLabel('Apply label "' + str(selectedLabel) + '" to all other unlabeled stops at this location?')
        question.setWordWrap(True)
        question.setObjectName('importantLabel')
        nobutton = QtWidgets.QPushButton('No')
        nobutton.setObjectName('smallButton')
        nobutton.setFixedWidth(nobutton.sizeHint().width())
        nobutton.clicked.connect(lambda: self.rejected.emit())
        yesbutton = QtWidgets.QPushButton('Yes')
        yesbutton.setObjectName('smallButton')
        yesbutton.setFixedWidth(yesbutton.sizeHint().width())
        yesbutton.clicked.connect(lambda: self.accept(dbConnection, stopId, selectedLabel))

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(10, 10, 10, 10)
        hlayout.addWidget(question)
        hlayout.addWidget(nobutton)
        hlayout.addSpacing(2)
        hlayout.addWidget(yesbutton)

        decorationlayout = QtWidgets.QHBoxLayout()
        decorationlayout.setContentsMargins(0, 0, 0, 0)
        decorationlayout.addWidget(indicator)
        decorationlayout.addLayout(hlayout)
        self.setLayout(decorationlayout)

    def accept(self, dbConnection, stopId, selectedLabel):
        dbupdates.newClusterPlaceTypeAssociation(dbConnection, stopId, selectedLabel)

        self.accepted.emit()