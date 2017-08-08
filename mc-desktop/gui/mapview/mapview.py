import os
from PyQt5 import QtCore, QtWidgets, QtQuickWidgets
from gui.mapview import splitwidget
from database import dbqueries
from appstatus.applicationstatus import ApplicationStatus
from database.dbconnection import DatabaseConnection
from helper.filehelper import FileHelper


class MapView(QtWidgets.QWidget):
    splitSignal = QtCore.pyqtSignal(ApplicationStatus, DatabaseConnection, int, str)
    # int, str: id of selected Movement and timestamp to split at (too large for int)

    def __init__(self, appStatus, dbConnection, alwaysShowEntirePath):
        QtWidgets.QWidget.__init__(self)
        PROJECT_DIR = FileHelper().get_project_cwd()
        self.alwaysShowEntirePath = alwaysShowEntirePath
        self.dbConnection = dbConnection

        # self.mapspace = QtQuickWidgets.QQuickWidget()
        # # set paths to location markers
        # self.mapspace.rootContext().setContextProperty("LocationMarkerSmall", os.path.join(PROJECT_DIR, 'res', 'location_marker_small.svg'))
        # self.mapspace.rootContext().setContextProperty("LocationMarker", os.path.join(PROJECT_DIR, 'res', 'location_marker.svg'))
        # self.mapspace.rootContext().setContextProperty("LocationMarkerSplit", os.path.join(PROJECT_DIR, 'res', 'location_marker_split.svg'))
        #
        # self.mapspace.setSource(QtCore.QUrl(os.path.join(PROJECT_DIR, 'gui', 'mapview', 'mymap.qml')))
        # self.mapspace.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)

        from gui.mapview.mapwidget import MapWidget
        self.mapspace = MapWidget()


        # placeholder for splitwidget to refer to when hiding
        self.split = QtWidgets.QFrame()

        # somelabel is necessary to be added to the same layout as map
        # otherwise a SIGSEGV occurrs
        # (which seems to be caused by an interaction between calendarWidget and MapWidget)
        somelabel = QtWidgets.QLabel('')
        somelabel.setFixedHeight(0)

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        self.vlayout.addWidget(self.mapspace, 1)
        self.vlayout.addWidget(somelabel, 0)
        self.setLayout(self.vlayout)

        # on startup show dayroute for initally selected date
        #self.showRouteOfCurrentDateOnMap(appStatus)
        #self.mapspace.rootObject().fitMap()

    def showRouteOfCurrentDateOnMap(self, appStatus):
        """ shows all paths of the current date as one long route of the day """
        currentDateEntries = appStatus.currentDateEntries
        self.split.setHidden(True)

        # dictlist is a list of dictpoints in latitude/longitude format:
        # i.e. [{"latitude": 30.5, "longitude": 40.2}, ... ]
        pathdictlist = []  # builds up one long path from all subpaths of that date
        markersdictlist = []

        for entry in currentDateEntries:
            if entry['type'] == 'Stop':
                clusterId = entry['value'].idCluster
                geom = dbqueries.getClusterForId(clusterId)
                markersdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})
            if entry['type'] == 'Movement':
                id = entry['value'].id
                subpath = dbqueries.getMovementPathForMovementId(self.dbConnection, id)
                for point in subpath:
                    geom = point['geom']
                    pathdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})

        self.mapspace.rootObject().clearAll()
        if self.alwaysShowEntirePath:
            self.mapspace.rootObject().setPathEntireDay(pathdictlist)
            self.mapspace.rootObject().setMarkersEntireDay(markersdictlist)
        else:
            self.mapspace.rootObject().setPathSelectedEntry(pathdictlist)
            self.mapspace.rootObject().setMarkersSelectedEntry(markersdictlist)

        self.mapspace.rootObject().fitMap()

    def showSelectedEntryOnMap(self, appStatus, entryIndex, isDoubleClicked):
        """ shows the currently selected entry of timeline on the map """
        currentDateEntry = appStatus.currentDateEntries[entryIndex]
        pathdictlist = []
        markersdictlist = []

        if currentDateEntry['type'] == 'Stop':
            self.split.setHidden(True)
            clusterId = currentDateEntry['value'].idCluster
            geom = dbqueries.getClusterForId(clusterId)
            markersdictlist.append({'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]})

        elif currentDateEntry['type'] == 'Movement':
            pathdictlistwithtime = []
            movementId = currentDateEntry['value'].id
            path = dbqueries.getMovementPathForMovementId(self.dbConnection, movementId)
            for point in path:
                geom = point['geom']
                dictpoint = {'longitude': geom['coordinates'][0], 'latitude': geom['coordinates'][1]}
                pathdictlist.append(dictpoint)
                timeatpoint = point['time']
                pathdictlistwithtime.append({'pathdictpoint': dictpoint, 'time': timeatpoint})
            markersdictlist.append(pathdictlist[0])
            markersdictlist.append(pathdictlist[-1])  # place a marker at beginning and end

            self.renewSplitWidget(movementId, pathdictlistwithtime, appStatus)
            self.split.setHidden(False)

        if self.alwaysShowEntirePath:
            # don't clear all but only the colored/selectedEntry path and markers
            self.mapspace.rootObject().clearOnlyPathAndMarkersOfSelectedEntry()
            self.mapspace.rootObject().setPathSelectedEntry(pathdictlist)
            self.mapspace.rootObject().setMarkersSelectedEntry(markersdictlist)
        else:
            self.mapspace.rootObject().clearAll()
            self.mapspace.rootObject().setPathSelectedEntry(pathdictlist)
            self.mapspace.rootObject().setMarkersSelectedEntry(markersdictlist)
        self.mapspace.rootObject().fitMap()

        if isDoubleClicked:
            if len(markersdictlist) > 0:
                self.mapspace.rootObject().fitMapToSelectedItems(markersdictlist[0]['latitude'],
                                                                 markersdictlist[0]['longitude'],
                                                                 markersdictlist[-1]['latitude'],
                                                                 markersdictlist[-1]['longitude'])
                #self.mapspace.rootObject().fitMap()

    def showSplitMarker(self, dictpoint):
        self.mapspace.rootObject().setSplitMarker(dictpoint)

    def renewSplitWidget(self, movementId, pathdictlistwithtime, appStatus):
        """ create new instance of splitWidget with new parameters
        (only setting the sliders' parameters would cause multiple widgets to pile up """
        if self.layout().itemAt(2):
            self.layout().removeWidget(self.split)
            self.split.setParent(None)
        self.split = splitwidget.SplitWidget(self, movementId, pathdictlistwithtime, appStatus, self.dbConnection)
        self.layout().insertWidget(1, self.split)
