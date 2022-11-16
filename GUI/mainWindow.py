from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from callWindow import CallWindow


ADRESSES=[['maria','11111111.11111111.11111111.11111111','3000'],
['joao','11111111.11111111.11111111.01111111','3000'],
['jose','11111111.11111111.11111111.11111110','3000']]

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("MainWindow")
        self.setGeometry(0, 0, 600, 400)
        self.dlg=None
        self.pagelayout=QVBoxLayout()
        
        self.initContact()

        self.widget=QWidget()
        self.widget.setLayout(self.pagelayout)
        self.setCentralWidget(self.widget)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.showCallDialog()
            
    def showCallDialog(self):
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle("Incoming Call")
        acceptcall=QPushButton(self)
        acceptcall.setIcon(QIcon("./images/accept.png"))
        declinecall=QPushButton(self)
        declinecall.setIcon(QIcon("./images/decline.png"))
        acceptcall.clicked.connect(self.showCall)
        declinecall.clicked.connect(self.declineCall)
        hbox=QHBoxLayout()
        hbox.addWidget(acceptcall)
        hbox.addWidget(declinecall)
        self.dlg.setLayout(hbox)
        self.dlg.exec()

    def initContact(self):
        for a in ADRESSES:
            label=QLabel(a[0],self)
            btn=QPushButton(self)
            btn.setFixedSize(100,50)
            btn.setIcon(QIcon("./images/accept.png"))
            btn.clicked.connect(self.showCall)
            contactlayout=QHBoxLayout()
            contactlayout.addWidget(label,alignment=Qt.AlignHCenter)
            contactlayout.addWidget(btn,alignment=Qt.AlignHCenter)
            self.pagelayout.addLayout(contactlayout)

    def declineCall(self):
        self.dlg.close()

    def showCall(self):
        self.call=CallWindow(self)
        self.call.show()
        if self.dlg:
            self.dlg.close()
        self.close()

