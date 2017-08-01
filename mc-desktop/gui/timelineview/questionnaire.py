from PyQt5 import QtWidgets, QtCore
from gui.style import styleparser
from helper import timehelper
from database import dbqueries, dbupdates


class Questionnaire(QtWidgets.QFrame):
    def __init__(self, appStatus, dbConnection):
        QtWidgets.QFrame.__init__(self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setProperty('hasFocus', False)
        stylesheetFilename = 'questionnairestylesheet.css'
        styleparser.StylesheetParser().setProcessedStyleSheet(stylesheetFilename, self)

        self.date_string = appStatus.currentDate
        self.date = timehelper.utc_to_timestamp(appStatus.currentDate)
        self.db_question1 = None
        self.db_question2 = None
        self.db_comment = None

        questionnaireresults = dbqueries.getQuestionnaireResultsForDate(dbConnection, self.date)
        if questionnaireresults:
            self.db_question1 = questionnaireresults.question_1
            self.db_question2 = questionnaireresults.question_2
            self.db_comment = questionnaireresults.comment

        self.question1 = Question("How typical is this sequence of <strong>locations</strong> for you?", self.db_question1, self)
        self.question2 = Question("How typical is this sequence of <strong>place types</strong> for you?", self.db_question2, self)
        self.comment = Comment(self.db_comment, self)

        self.applyButton = QtWidgets.QPushButton('Send')
        self.applyButton.setObjectName('okButton')
        self.applyButton.clicked.connect(lambda: self.submitQuestionnaireResults(dbConnection))

        # event Filter (not in use)
        for button in self.question1.scale.buttongroup.buttons():
            button.installEventFilter(self)
        for button in self.question2.scale.buttongroup.buttons():
            button.installEventFilter(self)
        self.comment.installEventFilter(self)
        self.installEventFilter(self)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(15, 15, 15, 15)
        vlayout.setSpacing(10)
        vlayout.addWidget(self.question1)
        vlayout.addWidget(self.question2)
        vlayout.addWidget(self.comment)
        vlayout.addWidget(self.applyButton)
        vlayout.setAlignment(self.applyButton, QtCore.Qt.AlignRight)
        self.setLayout(vlayout)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.setProperty('hasFocus', True)
            self.style().unpolish(self)
            self.style().polish(self)
            self.update()
        elif event.type == QtCore.QEvent.FocusOut:
            self.setProperty('hasFocus', False)
            self.style().unpolish(self)
            self.style().polish(self)
            self.update()
        return False

    def submitQuestionnaireResults(self, dbConnection):
        """ retrieves the current state of the questionnaire and sends it to database """
        date_timestamp = self.date

        button_q1 = self.question1.scale.buttongroup.checkedButton()
        button_q2 = self.question2.scale.buttongroup.checkedButton()
        q1 = button_q1.text() if button_q1 else None
        q2 = button_q2.text() if button_q2 else None
        comment = self.comment.textedit.toPlainText()
        dbupdates.updateQuestionnaireResults(dbConnection, date_timestamp, self.date_string, q1, q2, comment)


class Question(QtWidgets.QFrame):
    def __init__(self, string, db_question, parent):
        QtWidgets.QFrame.__init__(self, parent)

        wording = QtWidgets.QLabel(string)
        maxwidth = wording.width()
        self.setMaximumWidth(maxwidth)
        wording.setWordWrap(True)
        header = ScaleHeader()
        self.scale = Scale(db_question, self)

        gridlayout = QtWidgets.QGridLayout()
        gridlayout.setContentsMargins(0, 0, 0, 0)
        gridlayout.addWidget(wording, 1, 0)
        gridlayout.addWidget(header, 0, 1)
        gridlayout.addWidget(self.scale, 1, 1)
        self.setLayout(gridlayout)


class ScaleHeader(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        nottypical = QtWidgets.QLabel("not typical")
        verytypical = QtWidgets.QLabel("very typical")

        headerlayout = QtWidgets.QHBoxLayout()
        headerlayout.setContentsMargins(0,0,0,0)
        headerlayout.setSpacing(0)
        headerlayout.addWidget(nottypical)
        headerlayout.addWidget(verytypical)
        headerlayout.setAlignment(nottypical, QtCore.Qt.AlignLeft)
        headerlayout.setAlignment(verytypical, QtCore.Qt.AlignRight)
        self.setLayout(headerlayout)


class Scale(QtWidgets.QWidget):
    def __init__(self, db_question, parent):
        QtWidgets.QWidget.__init__(self, parent)

        self.buttongroup = QtWidgets.QButtonGroup()
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        for nr in [1, 2, 3, 4, 5]:
            button = QtWidgets.QRadioButton(str(nr))
            #button.setStyleSheet(" QRadioButton QLabel { subcontrol-position: top left; } ")
            self.buttongroup.addButton(button)
            hlayout.addWidget(button)

        if db_question:  # if not None
            for button in self.buttongroup.buttons():
                if int(button.text()) == db_question:
                    button.setChecked(True)

        self.setLayout(hlayout)


class Comment(QtWidgets.QWidget):
    def __init__(self, db_comment, parent):
        QtWidgets.QWidget.__init__(self, parent)

        label = QtWidgets.QLabel("Comment:")
        self.textedit = QtWidgets.QTextEdit()
        self.textedit.setFixedHeight(80)
        self.textedit.setText(db_comment)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.addWidget(label)
        vlayout.addWidget(self.textedit)
        self.setLayout(vlayout)



