import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from database import dbupdates


class ClusterAssociatorMessage(QtWidgets.QMessageBox):
    def __init__(self, address, selectedLabel, dbConnection, appStatus, stopId, associatedPlaceTypeId):
        QtWidgets.QMessageBox.__init__(self)
        self.setWindowTitle("Automatic labeling")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg')))
        self.setIcon(QtWidgets.QMessageBox.Question)

        text = " <p style='line-height: 120%;'> <strong> Automatic labeling: " + address + " </strong> <br/>"
        text += "Should we mark all occurrences of this location as <a style='color: red;'>'" + selectedLabel + "'</a>?<br/>"
        text += "(Multiple locations can be set as '" + selectedLabel + "'.) </p>"

        self.setText(text)
        self.setStandardButtons(QtWidgets.QMessageBox.Yes)
        self.addButton(QtWidgets.QMessageBox.No)
        self.setDefaultButton(QtWidgets.QMessageBox.Yes)

        # if usertestMode: no checkBox?
        checkbox = QtWidgets.QCheckBox('Disable automatic labeling and never show whis message again.')
        self.setCheckBox(checkbox)

        if self.exec() == QtWidgets.QMessageBox.Yes:
            dbupdates.newClusterPlaceTypeAssociation(dbConnection, stopId, associatedPlaceTypeId, selectedLabel)
            if checkbox.checkState() == QtCore.Qt.Checked:
                appStatus.automaticLabelingMode = False
                # TODO menu change checkbox
                AutomaticLabelingDisabledMessage().exec()
        else:
            if checkbox.checkState() == QtCore.Qt.Checked:
                appStatus.automaticLabelingMode = False
                # TODO menu change checkbox
                AutomaticLabelingDisabledMessage().exec()


class AutomaticLabelingDisabledMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)

        self.setWindowTitle("Automatic labeling disabled")
        self.setText("<p style='line-height: 120%;'>Automatic Labeling is now disabled. <br/>"
                     "You can reenable automatic labeling in the settings menu.</p>")