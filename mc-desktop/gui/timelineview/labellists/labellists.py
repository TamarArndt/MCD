import operator
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from semanticplacelabeling import semanticplacelabeling
from gui.style import iconfactory
from database import dbupdates, dbqueries
from gui.dialogs import clusterassociatormessage


# --------------------------------------------------------------------------------------------
# Stop
# --------------------------------------------------------------------------------------------
class StopLabelWidgetUsertestMode(QtWidgets.QWidget):
    def __init__(self, stopId, placeTypeLabel, isConfirmed, flagAutomaticLabeling,
                 dbConnection, appStatus, correspondingListItem, addressCommaSeparated):
        QtWidgets.QWidget.__init__(self)
        self.isConfirmed = isConfirmed
        self.address = addressCommaSeparated
        self.setProperty('isConfirmed', isConfirmed)

        self.combobox = StopLabelList(correspondingListItem, isConfirmed)

        # if automaticLabelingMode is disabled, change flagAutomaticLabeling only locally,
        # in order to ignore the automatic labeling cases
        if not appStatus.automaticLabelingMode:
            if flagAutomaticLabeling == 1:
                flagAutomaticLabeling = 0

        if isConfirmed:
            self.combobox.setCurrentText(placeTypeLabel)

        elif not isConfirmed:

            if appStatus.adaptivityMode:
                suggestions = self.getLabelSuggestionsIncludingClusterAssociationIfExistent(stopId, flagAutomaticLabeling,
                                                                                            placeTypeLabel)
                if not suggestions:  # if False returned: proceed the same way as in non-adaptive mode
                    print('no suggestions')
                    if flagAutomaticLabeling == 1:
                        print('no suggestions: only autolabel')
                        self.combobox.insertSeparator(0)
                        cluserAssociatedLabel = placeTypeLabel
                        icon = iconfactory.getStopLabelIcon(cluserAssociatedLabel)
                        self.combobox.insertItem(0, icon, cluserAssociatedLabel)
                        self.combobox.setItemData(0, getColorForConfidence(0.6), QtCore.Qt.BackgroundRole)
                    self.combobox.insertUnknownTop()
                    self.combobox.setCurrentText('Unknown')

                else:  # if suggestion worked
                    self.combobox.insertSeparator(0)
                    for suggestion in suggestions:
                        label = suggestion[0]
                        confidence = suggestion[1]
                        icon = iconfactory.getStopLabelIcon(label)
                        self.combobox.insertItem(0, icon, str(label))
                        self.combobox.setItemData(0, getColorForConfidence(confidence), QtCore.Qt.BackgroundRole)
                    self.combobox.insertUnknownTop()
                    self.combobox.setCurrentText('Unknown')

            elif not appStatus.adaptivityMode:
                if flagAutomaticLabeling == 1:
                    self.combobox.insertSeparator(0)
                    cluserAssociatedLabel = placeTypeLabel
                    icon = iconfactory.getStopLabelIcon(cluserAssociatedLabel)
                    self.combobox.insertItem(0, icon, cluserAssociatedLabel)
                    self.combobox.setItemData(0, getColorForConfidence(0.6), QtCore.Qt.BackgroundRole)
                self.combobox.insertUnknownTop()
                self.combobox.setCurrentText('Unknown')

        self.combobox.currentIndexChanged.connect(lambda: self.indexChangedAction(dbConnection, appStatus,
                                                                                  stopId, self.combobox.currentText()))

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(self.combobox)
        self.setLayout(vlayout)

    def setConfirmed(self):
        self.isConfirmed = True
        self.setProperty('isConfirmed', True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def getLabelSuggestionsIncludingClusterAssociationIfExistent(self, stopId, flagAutomaticLabeling, placeTypeLabel):
        """ returns a sorted list of the most probable labels
        if a cluster association exists, the associated label is integrated into the list, weighted by clusterAssociationWeight
        returns False if semantic place labeling can't provide the confidences """
        classificationresult = True #semanticplacelabeling.getLabelConfidencesForStopId(stopId)
        if not classificationresult:
            return False
        else:
            confidences = {'Friend & Family': 0.11539636746500072, 'Work': 0.08386752304450037, 'Home': 0.6879473186848128} #classificationresult['classification'][str(stopId)]
            # confidences is a dictionary of the form:
            # {'Friend & Family': 0.11539636746500072, 'Work': 0.08386752304450037, 'Home': 0.6879473186848128}
            if flagAutomaticLabeling == 1:  # there is a cluster-associated label
                clusterAssociatedLabel = placeTypeLabel
                clusterAssociationWeight = 0.2
                if clusterAssociatedLabel in confidences:
                    confidences[clusterAssociatedLabel] += clusterAssociationWeight
                    # make sure probability is not greater than 1
                    if confidences[clusterAssociatedLabel] > 1.0:
                        confidences[clusterAssociatedLabel] = 1.0
                else:
                    confidences[clusterAssociatedLabel] = clusterAssociationWeight
            # sort suggestions by confidence
            # confidencesSorted is a list of the form:
            # [('Work', 0.08386752304450037), ('Friend & Family', 0.11539636746500072), ('Home', 0.6879473186848128)]
            confidencesSorted = sorted(confidences.items(), key=operator.itemgetter(1))
            return confidencesSorted

    def indexChangedAction(self, dbConnection, appStatus, stopId, newPlaceTypeLabel):
        if not self.isConfirmed:
            self.setConfirmed()
        if not self.combobox.isConfirmed:
            self.combobox.confirm(appStatus)

        # update Label in db for this stop
        placeTypesKeyByValue = dict((v,k) for k, v in placeTypesList.items())
        newPlaceTypeId = placeTypesKeyByValue[newPlaceTypeLabel]
        dbupdates.updateStopLabel(dbConnection, appStatus, stopId, newPlaceTypeId, newPlaceTypeLabel)

        if not newPlaceTypeLabel == 'Detection is completely wrong':
            if appStatus.automaticLabelingMode:
                # if stops clusterId already associated with newPlaceTypeLabel: don't ask to associate again
                clusterId = dbqueries.getClusterIdFromStopId(dbConnection, stopId)
                alreadyAssociated = dbqueries.isClusterIdAssociatedWithPlaceTypeLabel(dbConnection, clusterId, newPlaceTypeLabel)
                if not alreadyAssociated:
                    logging.info("clusterAssociatorMessage")
                    clusterassociatormessage.ClusterAssociatorMessage(self.address, newPlaceTypeLabel,
                                                                      dbConnection, appStatus, stopId, newPlaceTypeId)


class StopLabelWidget(QtWidgets.QWidget):
    def __init__(self, stopId, placeTypeLabel, isConfirmed, flagAutomaticLabeling,
                 dbConnection, appStatus, correspondingListItem, addressCommaSeparated):
        QtWidgets.QWidget.__init__(self)
        self.isConfirmed = isConfirmed
        self.address = addressCommaSeparated
        self.setProperty('isConfirmed', isConfirmed)

        ''' if automaticLabelingMode is disabled, change flagAutomaticLabeling (only locally),
        in order to ignore the automatic labeling cases. This is only done for unconfirmed labels,
        thereby it is still visbile if something had been labeled automatically in the past '''
        if not appStatus.automaticLabelingMode:
            if flagAutomaticLabeling == 1:
                flagAutomaticLabeling = 0

        self.hintAutomaticLabeling = QtWidgets.QLabel('automatically labeled:            ')
        self.hintAutomaticLabeling.setParent(self)
        self.hintAutomaticLabeling.move(0, 8)
        self.hintAutomaticLabeling.setFixedHeight(self.hintAutomaticLabeling.sizeHint().height())
        self.labelConfirmButton = QtWidgets.QPushButton('Ok')
        self.labelConfirmButton.setParent(self)
        self.labelConfirmButton.setObjectName('labelConfirmButton')
        self.labelConfirmButton.setEnabled(False)
        self.labelConfirmButton.clicked.connect(lambda: self.confirmAction(dbConnection, appStatus, stopId, placeTypeLabel))

        # keep size when hidden
        retainSizePolicy = self.labelConfirmButton.sizePolicy()
        retainSizePolicy.setRetainSizeWhenHidden(True)
        self.labelConfirmButton.setSizePolicy(retainSizePolicy)

        self.combobox = StopLabelList(correspondingListItem, isConfirmed)

        if flagAutomaticLabeling == 0 or flagAutomaticLabeling == 3:
            self.hintAutomaticLabeling.hide()
            self.labelConfirmButton.hide()

        if flagAutomaticLabeling == 1:
            self.labelConfirmButton.setEnabled(True)

        if isConfirmed:
            self.combobox.setCurrentText(placeTypeLabel)

        elif not isConfirmed:
            if appStatus.adaptivityMode:
                suggestions = self.getLabelSuggestionsIncludingClusterAssociationIfExistent(stopId, flagAutomaticLabeling,
                                                                                            placeTypeLabel)
                if not suggestions:  # if False returned: proceed the same way as in non-adaptive mode
                    print('no suggestions provided')
                    if flagAutomaticLabeling == 1:
                        self.combobox.insertSeparator(0)
                        cluserAssociatedLabel = placeTypeLabel
                        icon = iconfactory.getStopLabelIcon(cluserAssociatedLabel)
                        self.combobox.insertItem(0, icon, cluserAssociatedLabel)
                        self.combobox.setItemData(0, getColorForConfidence(0.6), QtCore.Qt.BackgroundRole)
                        self.combobox.setCurrentIndex(0)
                        self.labelConfirmButton.setEnabled(True)
                        self.hintAutomaticLabeling.setHidden(False) #show()
                        self.hintAutomaticLabeling.setText('automatically labeled:')
                    else:
                        self.combobox.insertUnknownTop()
                        self.combobox.setCurrentText('Unknown')

                else:  # if suggestions did work
                    self.combobox.insertSeparator(0)
                    for suggestion in suggestions:
                        label = suggestion[0]
                        confidence = suggestion[1]
                        #confidencepercentage = ' ' + str( round((suggestion[1] * 100), 2)) + '%'
                        icon = iconfactory.getStopLabelIcon(label)
                        self.combobox.insertItem(0, icon, str(label)) # + confidencepercentage))
                        self.combobox.setItemData(0, getColorForConfidence(confidence), QtCore.Qt.BackgroundRole)
                    self.combobox.setCurrentIndex(0)
                    self.labelConfirmButton.setHidden(False) #show()
                    self.hintAutomaticLabeling.setHidden(False) #show()
                    self.labelConfirmButton.setEnabled(True)
                    self.hintAutomaticLabeling.setText('label with highest probability:')
                    # self.hintAutomaticLabeling.style().unpolish(self.hintAutomaticLabeling)
                    # self.hintAutomaticLabeling.style().polish(self.hintAutomaticLabeling)
                    # self.hintAutomaticLabeling.update()

            elif not appStatus.adaptivityMode:
                if flagAutomaticLabeling == 1:
                    self.combobox.insertSeparator(0)
                    cluserAssociatedLabel = placeTypeLabel
                    icon = iconfactory.getStopLabelIcon(cluserAssociatedLabel)
                    self.combobox.insertItem(0, icon, cluserAssociatedLabel)
                    self.combobox.setItemData(0, getColorForConfidence(0.6), QtCore.Qt.BackgroundRole)
                    self.combobox.setCurrentIndex(0)
                    self.labelConfirmButton.setEnabled(True)
                    self.hintAutomaticLabeling.setHidden(False) #show()
                    self.hintAutomaticLabeling.setText('automatically labeled:')
                else:
                    self.combobox.insertUnknownTop()
                    self.combobox.setCurrentText('Unknown')

        self.combobox.currentIndexChanged.connect(lambda: self.indexChangedAction(dbConnection, appStatus,
                                                                                  stopId, placeTypeLabel,
                                                                                  self.combobox.currentText()))

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.addWidget(self.combobox, 1)
        hlayout.setAlignment(self.combobox, QtCore.Qt.AlignLeft)
        hlayout.addSpacing(7)
        hlayout.addWidget(self.labelConfirmButton, 0)
        self.setLayout(hlayout)

    def setConfirmed(self):
        self.isConfirmed = True
        self.setProperty('isConfirmed', True)
        self.labelConfirmButton.setEnabled(False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        self.hintAutomaticLabeling.style().unpolish(self.hintAutomaticLabeling)
        self.hintAutomaticLabeling.style().polish(self.hintAutomaticLabeling)
        self.hintAutomaticLabeling.update()

    def getLabelSuggestionsIncludingClusterAssociationIfExistent(self, stopId, flagAutomaticLabeling, placeTypeLabel):
        """ returns a sorted list of the most probable labels
        if a cluster association exists, the associated label is integrated into the list, weighted by clusterAssociationWeight
        returns False if semantic place labeling can't provide the confidences """
        classificationresult = semanticplacelabeling.getLabelConfidencesForStopId(stopId)
        if not classificationresult:
            return False
        else:
            confidences = classificationresult['classification'][str(stopId)] #{'Friend & Family': 0.11539636746500072, 'Work': 0.08386752304450037, 'Home': 0.6879473186848128}
            # confidences is a dictionary of the form:
            # {'Friend & Family': 0.11539636746500072, 'Work': 0.08386752304450037, 'Home': 0.6879473186848128}
            if flagAutomaticLabeling == 1:  # there is a cluster-associated label
                clusterAssociatedLabel = placeTypeLabel
                clusterAssociationWeight = 0.2
                if clusterAssociatedLabel in confidences:
                    confidences[clusterAssociatedLabel] += clusterAssociationWeight
                    # make sure probability is not greater than 1
                    if confidences[clusterAssociatedLabel] > 1.0:
                        confidences[clusterAssociatedLabel] = 1.0
                else:
                    confidences[clusterAssociatedLabel] = clusterAssociationWeight
            # sort suggestions by confidence
            # confidencesSorted is a list of the form:
            # [('Work', 0.08386752304450037), ('Friend & Family', 0.11539636746500072), ('Home', 0.6879473186848128)]
            confidencesSorted = sorted(confidences.items(), key=operator.itemgetter(1))
            return confidencesSorted

    def indexChangedAction(self, dbConnection, appStatus, stopId, originalPlaceTypeLabel, newPlaceTypeLabel):
        if not self.isConfirmed:
            self.setConfirmed()
        if not self.combobox.isConfirmed:
            self.combobox.confirm(appStatus)

        if not originalPlaceTypeLabel == newPlaceTypeLabel:
            # because labels can occur twice in list
            self.hintAutomaticLabeling.hide()
            self.labelConfirmButton.hide()

        # update Label in db
        placeTypesKeyByValue = dict((v,k) for k, v in placeTypesList.items())
        newPlaceTypeId = placeTypesKeyByValue[newPlaceTypeLabel]
        dbupdates.updateStopLabel(dbConnection, appStatus, stopId, newPlaceTypeId, newPlaceTypeLabel)

        if not newPlaceTypeLabel == 'Detection is completely wrong':
            if appStatus.automaticLabelingMode:
                # if stops clusterId already associated with newPlaceTypeLabel: don't ask to associate again
                clusterId = dbqueries.getClusterIdFromStopId(dbConnection, stopId)
                alreadyAssociated = dbqueries.isClusterIdAssociatedWithPlaceTypeLabel(dbConnection, clusterId, newPlaceTypeLabel)
                if not alreadyAssociated:
                    clusterassociatormessage.ClusterAssociatorMessage(self.address, newPlaceTypeLabel,
                                                                      dbConnection, appStatus, stopId, newPlaceTypeId)

    def confirmAction(self, dbConnection, appStatus, stopId, origPlaceTypeLabel):
        if not self.isConfirmed:
            self.setConfirmed()
        if not self.combobox.isConfirmed:
            self.combobox.confirm(appStatus)

        confirmedLabel = self.combobox.currentText()
        placeTypesKeyByValue = dict((v,k) for k, v in placeTypesList.items())
        confirmedLabelId = placeTypesKeyByValue[confirmedLabel]
        dbupdates.updateStopLabel(dbConnection, appStatus, stopId, confirmedLabelId, confirmedLabel)

        if not confirmedLabel == 'Detection is completely wrong':
            if not origPlaceTypeLabel == confirmedLabel:
                # can be the case if cluster associated label also is the top suggestion
                if appStatus.automaticLabelingMode:
                    clusterassociatormessage.ClusterAssociatorMessage(self.address, confirmedLabel,
                                                                      dbConnection, appStatus, stopId, confirmedLabelId)


class StopLabelList(QtWidgets.QComboBox):
    def __init__(self, correspondingListItem, isConfirmed):
        QtWidgets.QComboBox.__init__(self)
        self.isDroppedDown = False
        self.isConfirmed = isConfirmed
        self.setProperty('isConfirmed', isConfirmed)
        self.correspondingListItem = correspondingListItem

        for item in sorted(placeTypesList.items())[1:]:  # without 'Unknown' label
            label = item[1]
            icon = iconfactory.getStopLabelIcon(label)
            self.addItem(icon, label)

        self.view()

    def focusInEvent(self, focusEvent):
        self.correspondingListItem.listWidget().setCurrentItem(self.correspondingListItem)

    def wheelEvent(self, wheelEvent):
        return self.correspondingListItem.listWidget().wheelEvent(wheelEvent)

    def showPopup(self):
        self.isDroppedDown = True
        return QtWidgets.QComboBox.showPopup(self)

    def hidePopup(self):
        self.isDroppedDown = False
        return QtWidgets.QComboBox.hidePopup(self)

    def keyPressEvent(self, keyEvent):
        if self.isDroppedDown:  # not working
            if keyEvent.key() == QtCore.Qt.Key_Space:
                self.hidePopup()
                self.hide()
            else:
                return QtWidgets.QComboBox.keyPressEvent(self, keyEvent)
        else:
            if keyEvent.key() == QtCore.Qt.Key_Space:
                self.showPopup()
            elif keyEvent.key() == QtCore.Qt.Key_Down or keyEvent.key() == QtCore.Qt.Key_Up:
                return self.correspondingListItem.listWidget().keyPressEvent(keyEvent)


    def insertUnknownTop(self):
        self.insertSeparator(0)
        icon = iconfactory.getStopLabelIcon('Unknown')
        self.insertItem(0, icon, 'Unknown')

    def confirm(self, appStatus):
        # remove 'Unknown'
        if self.itemText(0) == 'Unknown':
            self.blockSignals(True)
            self.removeItem(0)
            self.removeItem(0) # remove separator
            self.blockSignals(False)

        # property and repaint
        self.isConfirmed = True
        self.setProperty('isConfirmed', True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

        # change appStatus.labelingStatusForCurrentDate and notify timeline notification about change
        appStatus.labelingStatusForCurrentDate.numberOfLabeledStops += 1
        self.correspondingListItem.listWidget().numberOfLabeledEntriesChangedSignal.emit()


# --------------------------------------------------------------------------------------------
# Movement
# --------------------------------------------------------------------------------------------
class MovementLabelWidget(QtWidgets.QWidget):
    def __init__(self, movementId, travelModeLabel, isConfirmed, dbConnection, appStatus, correspondingListItem):
        QtWidgets.QWidget.__init__(self)
        self.isConfirmed = isConfirmed
        self.setProperty('isConfirmed', isConfirmed)

        self.combobox = MovementLabelList(travelModeLabel, correspondingListItem, isConfirmed)
        travelModesKeyByValue = dict((v,k) for k, v in travelModesList.items())
        self.combobox.currentIndexChanged.connect(lambda: self.indexChangedAction(movementId, dbConnection, appStatus,
                                                                                  travelModesKeyByValue[self.combobox.currentText()]))

        # layout
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.addWidget(self.combobox, 1)
        hlayout.setAlignment(self.combobox, QtCore.Qt.AlignLeft)

        if not appStatus.usertestMode:
            # spacing workaround
            labelConfirmButton = QtWidgets.QPushButton('Ok')
            labelConfirmButton.setObjectName('labelConfirmButton')
            labelConfirmButton.hide()
            retainSizePolicy = labelConfirmButton.sizePolicy()
            retainSizePolicy.setRetainSizeWhenHidden(True)
            labelConfirmButton.setSizePolicy(retainSizePolicy)
            hlayout.addSpacing(7)
            hlayout.addWidget(labelConfirmButton, 0)

        self.setLayout(hlayout)

    def setConfirmed(self):
        self.isConfirmed = True
        self.setProperty('isConfirmed', True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def indexChangedAction(self, movementId, dbConnection, appStatus, newTravelModeId):
        dbupdates.updateMovementLabel(dbConnection, movementId=movementId, newTravelModeId=newTravelModeId)
        if not self.isConfirmed:
            self.setConfirmed()
            self.combobox.confirm(appStatus)


class MovementLabelList(QtWidgets.QComboBox):
    def __init__(self, travelMode, correspondingListItem, isConfirmed):
        QtWidgets.QComboBox.__init__(self)
        self.isDroppedDown = False
        self.isConfirmed = isConfirmed
        self.setProperty('isConfirmed', isConfirmed)
        self.correspondingListItem = correspondingListItem

        for item in sorted(travelModesList.items()):
            label = item[1]
            if not (isConfirmed and label == 'Unknown'):
                icon = iconfactory.getMovementLabelIcon(label)
                self.addItem(icon, label)
        self.setCurrentText(travelMode)  # is 'Unknown' if label not yet confirmed

    def focusInEvent(self, focusEvent):
        self.correspondingListItem.listWidget().setCurrentItem(self.correspondingListItem)

    def wheelEvent(self, wheelEvent):
        return self.correspondingListItem.listWidget().wheelEvent(wheelEvent)

    def showPopup(self):
        self.isDroppedDown = True
        return QtWidgets.QComboBox.showPopup(self)

    def hidePopup(self):
        self.isDroppedDown = False
        return QtWidgets.QComboBox.hidePopup(self)

    def keyPressEvent(self, keyEvent):
        print('key pressed', 'is dropped down: ', self.isDroppedDown, 'key: ', keyEvent.key())
        if self.isDroppedDown:
            if keyEvent.key() == QtCore.Qt.Key_Space:
                print('key space')
                self.hidePopup()
                self.hide()
            else:
                return QtWidgets.QComboBox.keyPressEvent(self, keyEvent)
        else:
            if keyEvent.key() == QtCore.Qt.Key_Space:
                self.showPopup()
            elif keyEvent.key() == QtCore.Qt.Key_Down or keyEvent.key() == QtCore.Qt.Key_Up:
                return self.correspondingListItem.listWidget().keyPressEvent(keyEvent)





    def confirm(self, appStatus):
        # remove 'Unknown'
        for i in range(self.count()):
            if self.itemText(i) == 'Unknown':
                self.blockSignals(True)
                self.removeItem(i)
                self.blockSignals(False)

        # property and repaint
        self.isConfirmed = True
        self.setProperty('isConfirmed', True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

        # change appStatus.labelingStatusForCurrentDate and notify timeline notification about change
        appStatus.labelingStatusForCurrentDate.numberOfLabeledMovements += 1
        self.correspondingListItem.listWidget().numberOfLabeledEntriesChangedSignal.emit()


# --------------------------------------------------------------------------------------------
# other stuff  TODO: put this somewhere else
# --------------------------------------------------------------------------------------------

placeTypesList = {
    0: 'Unknown',
    1: 'Home',
    2: 'Education',
    3: 'Work',
    4: 'Friend & Family',
    5: 'Hotel',
    6: 'Restaurant',
    7: 'Nightlife',
    8: 'Grocery Store',
    9: 'Shop',
    10: 'Sport',
    11: 'Medical',
    12: 'Leisure',
    13: 'Transport Infrastructure',
    14: 'Other',
    15: 'Detection is completely wrong'
}

travelModesList = {
    1: 'Subway',
    2: 'Train',
    3: 'Tram',
    4: 'Pendelbus',
    5: 'Bus',
    6: 'Car',
    7: 'Plane',
    8: 'Walking',
    9: 'Cycling',
    10: 'Running',
    11: 'Motorcycle',
    12: 'Detection is completely wrong',
    13: 'Unknown'
}


def getColorForConfidence(confidence):
    a = 0
    if 0 < confidence < 0.15:
        a = 80
    if 0.15 < confidence < 0.25:
        a = 100
    if 0.25 < confidence < 0.5:
        a = 130
    if 0.5 < confidence < 0.75:
        a = 160
    if 0.75 < confidence < 1:
        a = 220
    return QtGui.QColor(41, 166, 0, a)
