from PyQt5 import QtCore

'''
currently not used
maybe more efficient alternative to signals back and forth for date management?
'''

class CurrentDateModel(QtCore.QAbstractItemModel):
    def __init__(self, appStatus, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.appStatus = appStatus
        self.refresh()

    def refresh(self):
        self.currentDate = self.appStatus.currentDate

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            return self.currentDate