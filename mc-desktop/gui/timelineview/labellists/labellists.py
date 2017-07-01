from PyQt5 import QtCore, QtWidgets
from gui.timelineview.labellists import labellistsmodels


# TODO add proxy models for sorting, side info and stuff

class LabelWidget(QtWidgets.QWidget):
    def __init__(self, type, label, flagAutomaticLabeling, dbConnection):
        QtWidgets.QWidget.__init__(self)

        #print(type, label, flagAutomaticLabeling, dbConnection)

        hintIfAutomaticallyLabeled = QtWidgets.QLabel('auto')
        confirmationButton = QtWidgets.QPushButton('OK/Done')


        if type == 'Stop':
            combobox = StopLabelList(label, dbConnection)
        elif type == 'Movement':
            combobox = MovementLabelList(label, dbConnection)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(combobox, 1)
        hlayout.addWidget(confirmationButton, 0)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(hintIfAutomaticallyLabeled, 0)
        vlayout.addLayout(hlayout, 1)
        vlayout.addSpacing(10)
        self.setLayout(vlayout)

        #vlayout.setAlignment(combobox, QtCore.Qt.AlignTop)
        ## TODO currently this is True for all stops
        #if automaticallyLabeled:
        #    autolabel.setText("<small>automatically labeled:</small>")



class StopLabelList(QtWidgets.QComboBox):
    def __init__(self, placeType, dbConnection):
        QtWidgets.QComboBox.__init__(self)

        stopmodel = labellistsmodels.StopLabelListModel(dbConnection)
        self.setModel(stopmodel)
        self.setCurrentText(placeType)

        self.setView(QtWidgets.QTableView())
        #stopmodel.setHeaderData(1, QtCore.Qt.Horizontal, "blubb", 1)



class MovementLabelList(QtWidgets.QComboBox):
    def __init__(self, travelMode, dbConnection):
        QtWidgets.QComboBox.__init__(self)

        movementmodel = labellistsmodels.MovementLabelListModel(dbConnection)
        self.setModel(movementmodel)
        self.setCurrentText(travelMode)


