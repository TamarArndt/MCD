import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.mapview import mapwidget
from database import dbqueries


class MapView(QtWidgets.QWidget):
    def __init__(self, appStatus, dbConnection):
        super(MapView, self).__init__()
        self.appStatus = appStatus
        self.dbConnection = dbConnection

        self.split = SplitWidget()
        self.mapspace = mapwidget.MapWidget(self.split)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(self.mapspace, 1)
        vlayout.addWidget(self.split, 0)
        self.setLayout(vlayout)


        # TODO: handle split hiding and showing
        ''' 
        self.split.setHidden(True) yields the error:
        Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
        
        maybe stack/overlay ontop of map instead of inserting in vlayout ?
        '''

        # on startup show dayroute for first date in database (appStatus.currentDate)
        self.showRouteOfCurrentDateOnMap()


    def showRouteOfCurrentDateOnMap(self):
        ''' shows all paths if the current date
        is connected to change of selected date '''
        #self.split.setHidden(True)
        currentDateEntries = self.appStatus.currentDateEntries

        pathgeoms = []  # is built to contain one long path from all subpaths of that date
        markergeoms = []
        for entry in currentDateEntries:
            if entry['type'] == 'Movement':
                id = entry['value'].id
                subpath = dbqueries.getMovementPathForMovementId(self.dbConnection, id)
                markergeoms.append(subpath[0]['geom'])  # place marker at each intersection of pathparts
                for point in subpath:
                    pathgeoms.append(point['geom'])
        markergeoms.append(pathgeoms[-1])
        self.mapspace.showOnMap(pathgeoms, markergeoms)



    def showSelectedEntryOnMap(self, entryIndex):
        ''' shows the currently selected entry of timeline on the map '''
        currentDateEntry = self.appStatus.currentDateEntries[entryIndex]

        if currentDateEntry['type'] == 'Stop':
            self.split.setHidden(True)
            clusterId = currentDateEntry['value'].idCluster
            cluster_area, centroid = dbqueries.getClusterForId(self.dbConnection, clusterId)
            markergeoms = [centroid[0]]
            self.mapspace.showOnMap([], markergeoms)
        elif currentDateEntry['type'] == 'Movement':
            self.split.setHidden(False)
            id = currentDateEntry['value'].id
            path = dbqueries.getMovementPathForMovementId(self.dbConnection, id)
            pathgeoms = []
            for point in path:
                pathgeoms.append(point['geom'])
            markergeoms = [pathgeoms[0], pathgeoms[-1]]  # place a marker at beginning and end
            self.mapspace.showOnMap(pathgeoms, markergeoms)
        else:
            pass



class SplitWidget(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.setToolTip("Split this movement, if you want to specify different travel modes for parts of it.")

        self.split_button = QtWidgets.QPushButton("Split")
        self.split_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.split_button)
        hlayout.addWidget(self.split_slider)
        self.setLayout(hlayout)

        self.split_button.setEnabled(False)

        with open(os.path.join(os.path.dirname(sys.modules['__main__'].__file__) , './gui/style/sliderstylesheet.css'), 'r', encoding='utf-8') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

            # TODO add timelabel above slider that shows time at corresponding pathpoint

    def setUp(self, path):
        ''' the slider is set up to represent the given path '''
        self.split_slider.setMinimum(0)
        self.split_slider.setMaximum(len(path) - 1)
        self.split_slider.setSingleStep(1)

        #self.split_slider.valueChanged.connect(map)

        # TODO with the slider movement also renew the time display


        #             # splitwidget setup
        #             self.splitwidget.split_slider.setMinimum(0)
        #             self.splitwidget.split_slider.setMaximum(len(self.dictlist) -1)
        #             self.splitwidget.split_slider.setSingleStep(1)
        #             self.splitwidget.split_slider.valueChanged.connect(self.split)
        #
        #             # create new markerItem (splitMarker) at minimumposition (in different color)
        #