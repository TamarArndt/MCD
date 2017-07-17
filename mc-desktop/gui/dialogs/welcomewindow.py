import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

class WelcomeDialog(QtWidgets.QDialog):
    def __init__(self, appStatus):
        QtWidgets.QDialog.__init__(self)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close)
        self.setWindowTitle("Willkommen")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg')))
        self.setModal(True)
        self.setMinimumWidth(550)

        logo = QtSvg.QSvgWidget(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'res', 'mc-logo.svg'))
        logo.setFixedSize(80, 80)

        text = QtWidgets.QTextEdit()

        # Versuchsbedingung 1: automatic labeling ON | adaptive label suggestions OFF
        content_versuchsbedingung1 = "<h1 align=center>Herzlich Willkommen!</h1>" \
                                     "<p>Schön, dass Sie helfen möchten, ein paar Daten zu kategorisieren.</p>" \
                                     "<p>In der mittleren Spalte des Programmfensters sehen Sie die Einträge zu dem " \
                                     "aktuell ausgewählten Tag, wie sie auch in Ihrem Kalender aufgezeichnet sind.</p>" \
                                     "<p>Das Programm versucht Ihnen, beim Kategorisieren der <i>Aufenthalte</i> zu helfen. " \
                                     "Wenn Sie eine Kategorie auswählen, werden Sie gefragt, " \
                                     "ob das Programm diese Kategorie für den Aufenthaltsort speichern soll. " \
                                     "Wenn Sie das bestätigen, wird Ihnen diese Kategorie das nächste mal, " \
                                     "wenn der Ort vorkommt wieder vorgeschlagen, " \
                                     "indem die Kategorie in der Liste hervorgehoben wird.</p>" \
                                     "<p>Wenn Sie alles verstanden haben, können Sie auf 'Ok' klicken " \
                                     "und mit dem Bearbeiten der Aufgaben beginnen.</p>"

        # Versuchsbedingung 2: automatic labeling ON | adaptive label suggestions ON
        content_versuchsbedingung2 = "<h1>Herzlich Willkommen!</h1>" \
                                     "<p>Schön, dass Sie helfen möchten, ein paar Daten zu kategorisieren.</p>" \
                                     "<p>In der mittleren Spalte des Programmfensters sehen Sie die Einträge" \
                                     "zu dem aktuell ausgewählten Tag, wie sie auch in Ihrem Kalender aufgezeichnet sind.</p>" \
                                     "<p>Das Programm versucht Ihnen, beim Kategorisieren der <i>Aufenthalte</i> zu helfen. " \
                                     "Wenn Sie eine Kategorie auswählen, werden Sie gefragt, " \
                                     "ob das Programm diese Kategorie für den Aufenthaltsort speichern soll. " \
                                     "Wenn Sie das bestätigen, wird diese Kategorie das nächste mal, " \
                                     "wenn der Ort vorkommt mit höherer Wahrschienlichkeit vorgeschlagen.</p>" \
                                     "<p>Außerdem werden die Daten mit einem Algorithmus evaluiert, " \
                                     "um die wahrscheinlichsten Kategorien pro Aufenthalt zu bestimmen. " \
                                     "Die drei wahrscheinlichsten Kategorien sind in den Listen jeweils hervorgehoben.</p>" \
                                     "<p>Wenn Sie alles verstanden haben, können Sie auf 'Ok' klicken " \
                                     "und mit dem Bearbeiten der Aufgaben beginnen.</p>"

        if not appStatus.adaptivityMode:
            text.textCursor().insertHtml(content_versuchsbedingung1)
        else:
            text.textCursor().insertHtml(content_versuchsbedingung2)

        text.setMinimumSize(QtCore.QSize(480, 340))

        okButton = QtWidgets.QPushButton('Ok')
        okButton.setObjectName('okButton')
        okButton.clicked.connect(self.accept)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setSpacing(20)
        hlayout.addWidget(logo, 1)
        hlayout.setAlignment(logo, QtCore.Qt.AlignTop)
        hlayout.addWidget(text, 2)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(10, 10, 10, 10)
        vlayout.setSpacing(20)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(okButton, 1)
        vlayout.setAlignment(logo, QtCore.Qt.AlignCenter)
        vlayout.setAlignment(okButton, QtCore.Qt.AlignRight)
        self.setLayout(vlayout)



        # non usertest mode:
        # maybe checkbox: don't show this on startup?
        #welcome = QtWidgets.QLabel('<h2>Welcome to the Mobility Companion Desktop Application</h2>')
        #welcometext = 'This application is for labeling data logged by the Mobility Companion Android/iOS Application.' \
         #             'The system will try to help you labeling your data. ...'

        #
        # info = 'Usertest mode: '
        # if appStatus.usertestMode:
        #     info += 'On \n'
        # else:
        #     info += 'Off \n'
        # info += 'Adaptivity mode: '
        # if appStatus.adaptivityMode:
        #     info += 'On'
        # else:
        #     info += 'Off'