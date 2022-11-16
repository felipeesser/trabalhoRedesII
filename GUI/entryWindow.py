
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainWindow import *

class EntryWindow(QMainWindow):
    def __init__(self):
        super(EntryWindow,self).__init__()
        self.setGeometry(0, 0, 600, 400)
        self.main=None
        self.setWindowTitle("EntryWindow")

        self.connectbtn=QPushButton('entrar',self)
        self.connectbtn.setFixedSize(100,50)
        self.connectbtn.clicked.connect(self.showMain)

        self.pagelayout=QVBoxLayout()
        self.pagelayout.addWidget(self.connectbtn,alignment=Qt.AlignHCenter)
        
        self.widget=QWidget()
        self.widget.setLayout(self.pagelayout)
        self.setCentralWidget(self.widget)
    
    def setAvailable(self):
        pass

    def showMain(self):
        self.setAvailable()
        self.main=MainWindow()
        self.main.show()
        self.close()