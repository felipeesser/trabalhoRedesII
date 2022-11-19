from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainWindow import *
from socket import *
import json 
import serverInfo

class EntryWindow(QMainWindow):
    def __init__(self,name,hostip,hostport):
        super(EntryWindow,self).__init__()
        
        self.name=name
        self.hostip,self.hostport=hostip,hostport
        self.serverip,self.serverport=serverInfo.SERVERIP,serverInfo.SERVERPORT

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
    
    def getAvailableAdresses(self):
        data=self.sendMessage((self.serverip, self.serverport), 'listar_contatos'.encode('utf-8'))
        formatted=json.loads(data.decode('utf-8').split(",",1)[-1].replace("'",''))
        contacts=[]
        for c in formatted:
            if c["nome"]!=self.name:
                contacts.append(c)
        return contacts

    def setAvailable(self):
        command="registro, %s, %s, %s"%(self.name,self.hostip,self.hostport)
        self.sendMessage((self.serverip, self.serverport), command.encode('utf-8'))

    def showMain(self):
        self.setAvailable()
        contacts=self.getAvailableAdresses()
        self.main=MainWindow(self.name,self.hostip,self.hostport,contacts)
        self.main.show()
        self.close()

    def sendMessage(self, address, message):
        serverSocket = create_connection(address)
        serverSocket.send(message)
        data = serverSocket.recv(1024)

        print('data: {}'.format(data.decode('utf-8')))
        return data