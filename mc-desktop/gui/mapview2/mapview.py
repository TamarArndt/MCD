from PyQt5 import QtCore, QtGui, QtWidgets
from gui.mapview2 import mapwidget, splitwidget
from database import dbqueries


class MapView(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QWidget.__init__(self)
        self.dbConnection = dbConnection

        self.mapspace = mapwidget.MapWidget()

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        self.vlayout.addWidget(self.mapspace)
        self.setLayout(self.vlayout)


    def showRouteOfCurrentDateOnMap(self, appStatus):
        """ shows all paths of the current date as one long route of the day """
        currentDateEntries = appStatus.currentDateEntries

        # dictlist is a list of dictpoints in latitude/longitude format:
        # i.e. [{"latitude": 30.5, "longitude": 40.2}, ... ]
        pathdictlist = []  # builds up one long path from all subpaths of that date
        markersdictlist = []

        for entry in currentDateEntries:
            if entry['type'] == 'Stop':
                clusterId = entry['value'].idCluster
                centroid = dbqueries.getClusterForId(self.dbConnection, appStatus, clusterId)
                geom = centroid[0]
                markersdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})
            if entry['type'] == 'Movement':
                id = entry['value'].id
                subpath = dbqueries.getMovementPathForMovementId(self.dbConnection, appStatus, id)
                for point in subpath:
                    geom = point['geom']
                    pathdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})

        self.mapspace.rootObject().clearAll()
        self.mapspace.rootObject().setPath(pathdictlist)
        self.mapspace.rootObject().setMarkers(markersdictlist)
        self.mapspace.rootObject().fitMap()

    def showSelectedEntryOnMap(self, appStatus, entryIndex):
        """ shows the currently selected entry of timeline on the map """
        currentDateEntry = appStatus.currentDateEntries[entryIndex]
        pathdictlist = []
        markersdictlist = []

        if currentDateEntry['type'] == 'Stop':
            clusterId = currentDateEntry['value'].idCluster
            centroid = dbqueries.getClusterForId(self.dbConnection, appStatus, clusterId)
            geom = centroid[0]
            markersdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})

        elif currentDateEntry['type'] == 'Movement':
            pathdictlistwithtime = []
            movementId = currentDateEntry['value'].id
            path = dbqueries.getMovementPathForMovementId(self.dbConnection, appStatus, movementId)
            for point in path:
                geom = point['geom']
                dictpoint = {'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]}
                pathdictlist.append(dictpoint)
                timeatpoint = point['time']
                pathdictlistwithtime.append({'pathdictpoint': dictpoint, 'time': timeatpoint})
            markersdictlist.append(pathdictlist[0])
            markersdictlist.append(pathdictlist[-1])  # place a marker at beginning and end

        self.mapspace.rootObject().clearAll()
        self.mapspace.rootObject().setPath(pathdictlist)
        self.mapspace.rootObject().setMarkers(markersdictlist)
        self.mapspace.rootObject().fitMap()

    def showSplitMarker(self, dictpoint):
        self.mapspace.rootObject().setSplitMarker(dictpoint)


    # def addSplitWidget(self):
    #     if self.layout().itemAt(1):
    #         pass
    #     else:
    #         self.split = splitwidget.SplitWidget()
    #         self.layout().insertWidget(1, self.split)
    #
    # def removeSplitWidget(self):
    #     if self.layout().itemAt(1):
    #         x = self.layout().itemAt(1)
    #         x.setParent(None)
    #         self.split.setParent(None)
    #         self.layout().removeWidget(x)
