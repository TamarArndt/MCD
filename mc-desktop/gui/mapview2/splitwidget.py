import os, sys
from PyQt5 import QtCore, QtWidgets
from helper import timehelper
from database import dbupdates

class SplitWidget(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        #self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.setToolTip("Split this movement, if you want to specify different travel modes for parts of it.")

        self.setFixedHeight(30)
        self.setStyleSheet('QFrame {background-color: firebrick;}')