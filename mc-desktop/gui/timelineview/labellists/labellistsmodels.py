from PyQt5 import QtCore
from gui.style import iconfactory


class StopLabelListModel(QtCore.QAbstractListModel):
    ''' represents data from PlaceType table of database
     and provides list of all stop labels '''
    def __init__(self, dbConnection, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.dbConnection = dbConnection
        self.refresh()

    def refresh(self):
        session = self.dbConnection.Session()
        self._stopLabels = session.query(self.dbConnection.PlaceType).all()

    def rowCount(self, parent):
        return len(self._stopLabels)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            place_type = self._stopLabels[row].place_type
            return "%s" % place_type
        if role == QtCore.Qt.DecorationRole:
            place_type = self._stopLabels[index.row()].place_type
            icon = iconfactory.getStopLabelIcon(place_type)
            return icon


class MovementLabelListModel(QtCore.QAbstractListModel):
    ''' represents data from TravelMode table of database
     and provides list of all movement labels '''
    def __init__(self, dbConnection, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.dbConnection = dbConnection
        self.refresh()

    def refresh(self):
        session = self.dbConnection.Session()
        self._movementLabels = session.query(self.dbConnection.TravelMode).all()

    def rowCount(self, parent):
        return len(self._movementLabels)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            travel_mode = self._movementLabels[row].travelMode
            return "%s" % travel_mode
        if role == QtCore.Qt.DecorationRole:
            travel_mode = self._movementLabels[index.row()].travelMode
            icon = iconfactory.getMovementLabelIcon(travel_mode)
            return icon

