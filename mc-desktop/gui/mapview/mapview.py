from PyQt5 import QtCore, QtGui, QtWidgets
from gui.mapview import mapwidget, splitwidget
from database import dbqueries


class MapView(QtWidgets.QWidget):
    splitSignal = QtCore.pyqtSignal()  # id of selected Movement and timestamp to split at
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QWidget.__init__(self)
        self.dbConnection = dbConnection

        self.split = splitwidget.SplitWidget(None)
        self.mapspace = mapwidget.MapWidget()

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        self.vlayout.addWidget(self.mapspace, 1)
        self.vlayout.addWidget(self.split, 0)
        self.setLayout(self.vlayout)

        # on startup show dayroute for first date in database (appStatus.currentDate)
        self.showRouteOfCurrentDateOnMap(appStatus)


    def showRouteOfCurrentDateOnMap(self, appStatus):
        """ shows all paths of the current date as one long route of the day """
        currentDateEntries = appStatus.currentDateEntries
        #self.removeSplitWidget()

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
            #self.removeSplitWidget()
            self.split.setHidden(True)
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

            # set up splitWidget
            # to keep splitWidgets piling up remove existing splitWidget first if there is one
            self.renewSplitWidget(movementId)
            #self.split.setHidden(False)
            self.split.setUp(self, pathdictlistwithtime)
            self.split.movementId = movementId

        self.mapspace.rootObject().clearAll()
        self.mapspace.rootObject().setPath(pathdictlist)
        self.mapspace.rootObject().setMarkers(markersdictlist)
        self.mapspace.rootObject().fitMap()

    def showSplitMarker(self, dictpoint):
        self.mapspace.rootObject().setSplitMarker(dictpoint)

    ''' 
    current workaround for hiding and showing the split widget:
    self.split.setHidden(True) yields the error:
    Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
    maybe stack/overlay ontop of map instead of inserting in vlayout ?
    '''
    def removeSplitWidget(self):
        if self.layout().itemAt(1):
            self.layout().removeWidget(self.split)
            self.split.setParent(None)

    def renewSplitWidget(self, movementId):
        if self.layout().itemAt(1):
            self.removeSplitWidget()
        self.split = splitwidget.SplitWidget(movementId)
        self.split.splitButton.clicked.connect(self.splitSignal.emit)
        self.layout().insertWidget(1, self.split)

