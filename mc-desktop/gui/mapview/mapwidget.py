import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtQuickWidgets


class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self):
        QtQuickWidgets.QQuickWidget.__init__(self)

        self.setSource(QtCore.QUrl(os.path.join(os.path.dirname(__file__) , 'mymap.qml')))
        self.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)