import os
from PyQt5 import QtQuickWidgets, QtCore
from helper.filehelper import FileHelper

class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self):
        QtQuickWidgets.QQuickWidget.__init__(self)
        PROJECT_DIR = FileHelper().get_project_cwd()

        self.rootContext().setContextProperty("LocationMarkerSmall", os.path.join(PROJECT_DIR, 'res', 'location_marker_small.svg'))
        self.rootContext().setContextProperty("LocationMarker", os.path.join(PROJECT_DIR, 'res', 'location_marker.svg'))
        self.rootContext().setContextProperty("LocationMarkerSplit", os.path.join(PROJECT_DIR, 'res', 'location_marker_split.svg'))

        self.setSource(QtCore.QUrl(os.path.join(PROJECT_DIR, 'gui', 'mapview', 'mymap.qml')))
        self.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
