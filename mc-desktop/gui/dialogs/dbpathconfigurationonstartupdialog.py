import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from database import dbconnection
from configuration import configuration
from helper.filehelper import FileHelper

class DatabasePathConfig(QtWidgets.QDialog):
    def __init__(self, db_path_default):
        QtWidgets.QDialog.__init__(self)
        self.db_path = db_path_default

        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.reject)

        self.setWindowTitle("Database path configuration")
        PROJECT_DIR = FileHelper().get_project_cwd()
        self.setWindowIcon(QtGui.QIcon(os.path.join(PROJECT_DIR, 'res', 'mc-logo.svg')))
        self.setModal(True)
        self.setMaximumHeight(300)

        # ------------------------------------------------------------
        dbicon = QtSvg.QSvgWidget(os.path.join(PROJECT_DIR, 'res', 'database.svg'))
        dbicon.setFixedSize(40, 40)
        #database.svg: <Madebyoliver> http://www.flaticon.com, licensed by Creative Commons BY 3.0
        text = QtWidgets.QLabel("<p> Please specify the database file you would like to use or just press Continue "
                                "to use the given default database file. </p>")
        text.setWordWrap(True)

        pathfield = QtWidgets.QLineEdit(str(db_path_default))
        pathfield.setReadOnly(True)
        pathfield.setDragEnabled(True)
        changedefaultbutton = QtWidgets.QPushButton('change default')

        self.errormessage = QtWidgets.QLabel('')
        self.errormessage.setProperty('type', 'error')
        self.okbutton = QtWidgets.QPushButton('Continue')
        self.okbutton.setObjectName('okButton')
        self.okbutton.clicked.connect(lambda: self.acceptIfValidated(self.validateInput(self.db_path), self.db_path))

        hlayout1 = QtWidgets.QHBoxLayout()
        hlayout1.addWidget(dbicon)
        hlayout1.addWidget(text)

        hlayout2 = QtWidgets.QHBoxLayout()
        hlayout2.addWidget(pathfield)
        hlayout2.addWidget(changedefaultbutton)
        hlayout2.setAlignment(changedefaultbutton, QtCore.Qt.AlignRight)

        hlayout3 = QtWidgets.QHBoxLayout()
        hlayout3.addWidget(self.errormessage)
        hlayout3.addWidget(self.okbutton)
        hlayout3.setAlignment(self.okbutton, QtCore.Qt.AlignRight)

        # ------------------------------------------------------------
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(20, 20, 20, 20)
        vlayout.setSpacing(20)
        vlayout.addWidget(QtWidgets.QLabel("<h2> Welcome to the Mobility Companion Desktop App </h2> "))
        vlayout.addLayout(hlayout1)
        vlayout.addLayout(hlayout2)
        vlayout.addLayout(hlayout3)
        self.setLayout(vlayout)

        dbfiledialog = QtWidgets.QFileDialog()
        dbfiledialog.setNameFilter('*.db')
        changedefaultbutton.clicked.connect(lambda: self.getNewDbFilePath(pathfield, dbfiledialog))

    def getNewDbFilePath(self, pathfield, filedialog):
        if filedialog.exec():
            new_db_path = filedialog.selectedFiles()[0]
            pathfield.setText(new_db_path)
            self.validateInput(new_db_path)
            self.db_path = new_db_path

    def validateInput(self, dbpath):
        if not os.path.exists(dbpath):
            self.errormessage.setText("The given file does not exist. Please specify another one.")
            self.okbutton.setEnabled(False)
            return False
        else:
            try:
                dbconnection.DatabaseConnection(dbpath)
            except Exception as e:
                self.errormessage.setText('The given database file seems not to have the right content. <br>'
                                          'Please use a database that contains sensor data logged by the Mobility Companion Android/iOS App.')
                self.okbutton.setEnabled(False)
                return False
            self.errormessage.setText('')
            self.okbutton.setEnabled(True)
            return True

    def acceptIfValidated(self, isValidated, newDbPath):
        if isValidated:
            # write changed dbpath to configuration.ini
            configuration.updateGivenPathsInConfigFile([newDbPath])
            self.accept()
