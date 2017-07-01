from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtQuickWidgets
import os
#from gui.timelineview.timeline import timelinequeries, timeline

class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self):
        QtQuickWidgets.QQuickWidget.__init__(self)

        self.setSource(QtCore.QUrl(os.path.join(os.path.dirname(__file__) , './mymap.qml')))
        self.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)


#             # show splitwidget
#             self.splitwidget.setHidden(False)
#             # splitwidget setup
#             self.splitwidget.split_slider.setMinimum(0)
#             self.splitwidget.split_slider.setMaximum(len(self.dictlist) -1)
#             self.splitwidget.split_slider.setSingleStep(1)
#             self.splitwidget.split_slider.valueChanged.connect(self.split)
#
#             # create new markerItem (splitMarker) at minimumposition (in different color)
#
#             self.root.clearAll()
#             self.root.setPath(self.dictlist)
#             self.root.setMarkers([self.dictlist[0], self.dictlist[-1]]) # markers at first and last point of path
#
#             # center and zoom map such that both ends of path are visible
#             self.root.fitMap()
#
#
#     def split(self):
#         splitslider = self.splitwidget.split_slider
#         splitbutton = self.splitwidget.split_button
#         slidervalue = splitslider.value()
#
#         # split button is only enabled when slider is at a splitable position
#         # disabled if slidervalue = min or max, else enabled
#         if splitslider.minimum() < slidervalue < splitslider.maximum():
#             splitbutton.setEnabled(True)
#             # get pathpoint corresponding to slidervalue and place the green SplitMarker there in qml
#             dictpoint = self.dictlist[slidervalue]
#             self.root.setSplitMarker(dictpoint)
#         else:
#             splitbutton.setEnabled(False)
#
#
#             #splitbutton.clicked().connect()
#
#
#             # CONNECT SPLITBUTTON
#             #splitbutton.pushed.connect -> update Database somehow and update timeline (don't know how)
#
#     def splitMovementInTimeline(self):
#         pass
#         # TODO write this function in timeline
#         # remove current movement and add two new ones
#
#         # -------------------------------------------------------------------------------
#         # SPLIT:
#         #
#         # 1. when a mvmt is selected, make split button+slider visible
#         # 2. add a second marker (different color) to the paths starting point
#         # 3. when slider is moved, move the marker along the path (pathpoint by pathpoint)
#         # 4. split button is only enabled, when sliderposition/markerposition is not begin or end of path
#         # 5. when split button is pushed:
#         #    5.1 return that pathpoint  -> renew timeline from there (and report back to db)
#         #    5.2 leave the marker
#         # -------------------------------------------------------------------------------
#
#
# '''
# QSlider:
# - make its range the length of the pathpointslist (QSlider only handles integers!)
# - setSingleStep(1)
# - setPageStep(5) ? vllt ? (or set pagestep to length of list -> begin/end, and create ticks here (tickInterval)
# - setMinimum() = 0
# - setMaximum() = length of pathpointslist
#
# each step cooresponds to an element of pathpointslist
# QSliderValue = i -> pathpointslist[i]
#
# valueChanged()	Emitted when the slider's value has changed. The tracking() determines whether this signal is emitted during user interaction.
# setTracking(True) : this way slider emits valueChanged signal while being tracked (not only on mouse release)
#
# sliderPressed()	Emitted when the user starts to drag the slider.
# sliderMoved()	Emitted when the user drags the slider.
# sliderReleased()	Emitted when the user releases the slider.
#
# maybe later:
# triggerAction() to simulate the effects of clicking (useful for shortcut keys)
# '''
