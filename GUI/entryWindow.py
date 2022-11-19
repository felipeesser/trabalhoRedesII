
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainWindow import *
from socket import *

class EntryWindow(QMainWindow):
    def __init__(self):
        super(EntryWindow,self).__init__()
        self.setGeometry(0, 0, 600, 400)
        self.main=None
        self.setWindowTitle("EntryWindow")
        self.nameLabel = QLabel('Nome:', self)
        self.nameInput = QLineEdit(self)
        self.portLabel = QLabel('Porta desejada:', self)
        self.desiredPortInput = QLineEdit(self)
        self.connectbtn=QPushButton('entrar', self)
        self.connectbtn.setFixedSize(100,50)
        self.connectbtn.clicked.connect(self.showMain)
        
        self.pagelayout=QVBoxLayout()
        self.pagelayout.addWidget(self.nameLabel,alignment=Qt.AlignCenter)
        self.pagelayout.addWidget(self.nameInput,alignment=Qt.AlignCenter)
        self.pagelayout.addWidget(self.portLabel,alignment=Qt.AlignCenter)
        self.pagelayout.addWidget(self.desiredPortInput,alignment=Qt.AlignCenter)
        self.pagelayout.addWidget(self.connectbtn,alignment=Qt.AlignCenter)
        
        self.widget=QWidget()
        self.widget.setLayout(self.pagelayout)
        self.setCentralWidget(self.widget)
    
    def setAvailable(self):
        name = self.nameInput.text()
        desiredPort = self.desiredPortInput.text()
        registryServerSocket = create_connection(('127.0.0.1', 9999))
        registryServerSocket.send('registro, {}, 127.0.0.1, {}'.format(name, desiredPort).encode('utf-8'))
        data = registryServerSocket.recv(1024).decode('utf-8')
        if 'inserido' in data: print('success on insert')

    def showMain(self):
        self.setAvailable()
        self.main=MainWindow()
        self.main.show()
        self.close()