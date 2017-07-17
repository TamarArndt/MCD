import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from database import dbconnection
from configuration import configuration

class PathConfigurationDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.setWindowTitle("Filepath settings")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg')))
        self.setModal(True)
        self.setMinimumWidth(550)

        # currentDefaultPaths:
        self.newDbPath, self.newJarPath, self.newModelPath = self.defaultDbPath, self.defaultJarPath, self.defaultModelPath = configuration.accessConfig()


        # ----------------------------------------------------
        # DATABASE FIILE
        dbtext = QtWidgets.QLabel('Please be aware, that if you change the database path the application needs to be restartet for the new setting to take effect. You can always specify a different database path on startup.')
        dbtext.setWordWrap(True)
        dblayout1 = QtWidgets.QHBoxLayout()
        dblayout1.addWidget(QtWidgets.QLabel('<strong>database file</strong>'))

        self.dberrormessage = QtWidgets.QLabel('')
        self.dberrormessage.setProperty('type', 'error')
        self.dberrormessage.setWordWrap(True)

        dbpathedit = QtWidgets.QLineEdit(str(self.defaultDbPath))
        dbpathedit.setReadOnly(True)
        dbpathedit.setDragEnabled(True)
        dbchangebutton = QtWidgets.QPushButton('change default')

        dblayout = QtWidgets.QHBoxLayout()
        dblayout.addWidget(dbpathedit)
        dblayout.addWidget(dbchangebutton)

        dbfiledialog = QtWidgets.QFileDialog(self)
        dbfiledialog.setNameFilter('*.db')
        dbchangebutton.clicked.connect(lambda: self.getNewDbFilePath(dbpathedit, dbfiledialog))

        # ----------------------------------------------------
        # JAR FILE
        jarmodeltext = QtWidgets.QLabel('The .jar and .model files are used for generating label suggestions in adaptivity mode. If adaptivity mode is turned off, changing their paths will not have any effect.')
        jarmodeltext.setWordWrap(True)

        jarpathedit = QtWidgets.QLineEdit(str(self.defaultJarPath))
        jarpathedit.setReadOnly(True)
        jarpathedit.setDragEnabled(True)
        jarchangebutton = QtWidgets.QPushButton('change default')

        jarlayout = QtWidgets.QHBoxLayout()
        jarlayout.addWidget(jarpathedit)
        jarlayout.addWidget(jarchangebutton)

        jarfiledialog = QtWidgets.QFileDialog(self)
        jarfiledialog.setNameFilter('*.jar')
        jarchangebutton.clicked.connect(lambda: self.getNewJarFilePath(jarpathedit, jarfiledialog))

        # ----------------------------------------------------
        # MODEL FILE
        modelpathedit = QtWidgets.QLineEdit(str(self.defaultModelPath))
        modelpathedit.setReadOnly(True)
        modelpathedit.setDragEnabled(True)
        modelchangebutton = QtWidgets.QPushButton('change default')

        modellayout = QtWidgets.QHBoxLayout()
        modellayout.addWidget(modelpathedit)
        modellayout.addWidget(modelchangebutton)

        modelfiledialog = QtWidgets.QFileDialog(self)
        modelfiledialog.setNameFilter('*.model')
        modelchangebutton.clicked.connect(lambda: self.getNewModelFilePath(modelpathedit, modelfiledialog))

        # ----------------------------------------------------
        # Cancel and Done button
        cancelbutton = QtWidgets.QPushButton("Cancel")
        cancelbutton.clicked.connect(self.reject)
        self.okbutton = QtWidgets.QPushButton("Done")
        self.okbutton.setObjectName('okButton')
        self.okbutton.clicked.connect(self.submitChanges)
        QtWidgets.QShortcut(QtGui.QKeySequence("Enter"), self, self.okbutton.click)

        buttonlayout = QtWidgets.QHBoxLayout()
        buttonlayout.addWidget(cancelbutton)
        buttonlayout.addWidget(self.okbutton)
        buttonlayout.setAlignment(cancelbutton, QtCore.Qt.AlignLeft)
        buttonlayout.setAlignment(self.okbutton, QtCore.Qt.AlignRight)

        # LAYOUT ------------------------------------------------------------------
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(20, 20, 20, 20)
        vlayout.setSpacing(5)
        vlayout.addWidget(QtWidgets.QLabel('<h2> Filepath settings </h2>'))
        vlayout.addSpacing(20)
        #vlayout.addWidget(SeparatorLine())
        vlayout.addSpacing(20)

        vlayout.addWidget(QtWidgets.QLabel('<strong>database file</strong>'))
        vlayout.addWidget(dbtext)
        vlayout.addLayout(dblayout)
        vlayout.addWidget(self.dberrormessage)
        vlayout.addWidget(SeparatorLine())
        vlayout.addSpacing(20)

        vlayout.addWidget(jarmodeltext)
        vlayout.addWidget(QtWidgets.QLabel('<strong>.jar file</strong>'))
        vlayout.addLayout(jarlayout)
        vlayout.addWidget(QtWidgets.QLabel('<strong>.model file</strong>'))
        vlayout.addLayout(modellayout)
        vlayout.addSpacing(20)
        #vlayout.addWidget(SeparatorLine())
        vlayout.addSpacing(20)

        vlayout.addLayout(buttonlayout)
        self.setLayout(vlayout)

    # ----------------------------------------------------

    def getNewDbFilePath(self, lineedit, filedialog):
        if filedialog.exec():
            newpath = filedialog.selectedFiles()[0]
            lineedit.setText(newpath)
            if not self.newDbPath == newpath:
                self.validateDbPath(newpath)
                self.newDbPath = newpath
            if not self.defaultDbPath == newpath:
                self.okbutton.setText("Close App") #Restart")
            else:
                self.okbutton.setText("Done")

    def getNewJarFilePath(self, lineedit, filedialog):
        if filedialog.exec():
            newpath = filedialog.selectedFiles()[0]
            lineedit.setText(newpath)
            self.newJarPath = newpath

    def getNewModelFilePath(self, lineedit, filedialog):
        if filedialog.exec():
            newpath = filedialog.selectedFiles()[0]
            lineedit.setText(newpath)
            self.newModelPath = newpath

    def validateDbPath(self, dbpath):
        if not os.path.exists(dbpath):
            self.dberrormessage.setText("The given file does not exist. Please specify another one.")
            self.okbutton.setEnabled(False)
            return False
        else:
            try:
                dbconnection.DatabaseConnection(dbpath)
            except Exception as e:
                self.dberrormessage.setText('The given database file seems not to have the right content. <br>'
                                          'Please use a database that contains sensor data logged by the Mobility Companion Android/iOS App.')
                self.okbutton.setEnabled(False)
                return False
            self.dberrormessage.setText('')
            self.okbutton.setEnabled(True)
            return True

    def submitChanges(self):
        # write changes to configuration.ini
        pathsToChange = []
        if not self.newDbPath == self.defaultDbPath:
            pathsToChange.append(self.newDbPath)
        if not self.newJarPath == self.defaultJarPath:
            pathsToChange.append(self.newJarPath)
        if not self.newModelPath == self.defaultModelPath:
            pathsToChange.append(self.newModelPath)
        configuration.updateGivenPathsInConfigFile(pathsToChange)

        # restart if required
        if self.okbutton.text() == 'Done':
            self.accept()
        elif self.okbutton.text() == 'Close App': #Restart':
            QtWidgets.qApp.exit()


class SeparatorLine(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.setStyleSheet(' QFrame {color: lightgray;}')
        self.setLineWidth(1)
        self.setFixedHeight(1)

