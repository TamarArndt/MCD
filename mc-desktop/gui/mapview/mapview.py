import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.mapview import mapwidget, splitwidget
from database import dbqueries


class MapView(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        super(MapView, self).__init__()
        self.appStatus = appStatus
        self.dbConnection = dbConnection

        self.split = splitwidget.SplitWidget()
        self.mapspace = mapwidget.MapWidget()

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        self.vlayout.addWidget(self.mapspace, 1)
        self.vlayout.addWidget(self.split, 0)
        self.setLayout(self.vlayout)


        # on startup show dayroute for first date in database (appStatus.currentDate)
        self.showRouteOfCurrentDateOnMap()



    def showRouteOfCurrentDateOnMap(self):
        ''' shows all paths of the current date as one long route of the day '''
        currentDateEntries = self.appStatus.currentDateEntries

        # dictlist is a list of dictpoints in latitude/longitude format:
        # i.e. [{"latitude": 30.5, "longitude": 40.2}, ... ]
        pathdictlist = []  # builds up one long path from all subpaths of that date
        markersdictlist = []

        for entry in currentDateEntries:
            if entry['type'] == 'Movement':
                id = entry['value'].id
                subpath = dbqueries.getMovementPathForMovementId(self.dbConnection, id)
                geom = subpath[0]['geom']
                # place a marker at the start of each subpath
                markersdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})
                for point in subpath:
                    geom = point['geom']
                    pathdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})
        markersdictlist.append(pathdictlist[-1])

        self.mapspace.rootObject().clearAll()
        self.mapspace.rootObject().setPath(pathdictlist)
        self.mapspace.rootObject().setMarkers(markersdictlist)
        self.mapspace.rootObject().fitMap()



    def showSelectedEntryOnMap(self, entryIndex):
        ''' shows the currently selected entry of timeline on the map '''
        currentDateEntry = self.appStatus.currentDateEntries[entryIndex]

        pathdictlist = []
        markersdictlist = []

        if currentDateEntry['type'] == 'Stop':
            self.removeSplitWidget()
            #self.split.setHidden(True)
            clusterId = currentDateEntry['value'].idCluster
            centroid = dbqueries.getClusterForId(self.dbConnection, clusterId)
            geom = centroid[0]
            markersdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})

        elif currentDateEntry['type'] == 'Movement':
            pathdictlistwithtime = []
            id = currentDateEntry['value'].id
            path = dbqueries.getMovementPathForMovementId(self.dbConnection, id)
            for point in path:
                geom = point['geom']
                dictpoint = {'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]}
                pathdictlist.append(dictpoint)
                timeatpoint = point['time']
                pathdictlistwithtime.append({'pathdictpoint': dictpoint, 'time': timeatpoint})
            markersdictlist.append(pathdictlist[0])
            markersdictlist.append(pathdictlist[-1])  # place a marker at beginning and end

            # set up splitWidget
            # to keep splitWidgets piling up remove existing splitWidget first if there is one
            self.renewSplitWidget()
            self.split.setHidden(False)
            self.split.setUp(self, pathdictlistwithtime)

        self.mapspace.rootObject().clearAll()
        self.mapspace.rootObject().setPath(pathdictlist)
        self.mapspace.rootObject().setMarkers(markersdictlist)
        self.mapspace.rootObject().fitMap()


    def showSplitMarker(self, dictpoint):
        self.mapspace.rootObject().setSplitMarker(dictpoint)


    # what a splitwidgetsetup wants:
    # - pathwithtime: [ {'pathdictpoint': {'longitude': 9.05 ,'latitude': 48.81}, 'time': 13853481938 }, {}, {}, ...]


    # workaround for hiding split widget ?
    ''' 
    self.split.setHidden(True) yields the error:
    Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
    maybe stack/overlay ontop of map instead of inserting in vlayout ?
    '''
    def removeSplitWidget(self):
        self.layout().removeWidget(self.split)
        self.split.setParent(None)

    def renewSplitWidget(self):
        print(self.layout().itemAt(1))
        if self.layout().itemAt(1):
            self.removeSplitWidget()
        print(self.layout().itemAt(1))
        self.split = splitwidget.SplitWidget()
        self.layout().insertWidget(1, self.split)

