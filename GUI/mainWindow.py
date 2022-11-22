from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from callWindow import *
import serverInfo
from socket import *
import json

class MainWindow(QMainWindow):
    def __init__(self,name,hostip,hostport,inicontacts):
        super(MainWindow,self).__init__()
        self.setWindowTitle("MainWindow")
        self.setGeometry(0, 0, 600, 400)

        self.name=name
        self.serverip,self.serverport=serverInfo.SERVERIP,serverInfo.SERVERPORT
        self.hostip,self.hostport=hostip,hostport
        self.contacts=inicontacts

        self.calldlg=None
        self.pagelayout=QVBoxLayout()
        
        
        self.initContacts()

        self.initSocket()
        self.widget=QWidget()
        self.widget.setLayout(self.pagelayout)
        self.setCentralWidget(self.widget)

    def sendMessage(self, address, message):
        serverSocket = create_connection(address)
        serverSocket.send(message)
        data = serverSocket.recv(1024)

        print('data: {}'.format(data.decode('utf-8')))
        return data

    def closeEvent(self, event):
        command="remocao, %s"%(self.name)
        self.sendMessage((self.serverip, self.serverport), command.encode('utf-8'))

    def reload(self):
        
        self.deleteContactBtns()
        self.getAvailableAdresses()
        
    def deleteContactBtns(self):
        for i in reversed(range(self.pagelayout.count())): 
            for j in range(self.pagelayout.itemAt(i).count()):
                self.pagelayout.itemAt(i).itemAt(j).widget().deleteLater()

    def getAvailableAdresses(self):
        data=self.sendMessage((self.serverip, self.serverport), 'listar_contatos'.encode('utf-8'))
        formatted=json.loads(data.decode('utf-8').split(",",1)[-1].replace("'",''))
        contacts=[]
        for c in formatted:
            if c["nome"]!=self.name:
                contacts.append(c)
        self.contacts=contacts
        self.initContacts()
        
            
    def showCallDialog(self,host,port):
        print(host,port)
        self.calldlg = QDialog(self)
        self.calldlg.setWindowTitle("Incoming Call")
        pagelayout=QVBoxLayout()
        
        lbl=QLabel("Ligação recebida",self)
        pagelayout.addWidget(lbl)
        
        btnslayout=QHBoxLayout()
        acceptcall=QPushButton(self)
        acceptcall.setIcon(QIcon("./images/accept.png"))
        acceptcall.clicked.connect(lambda:self.acceptCall(host,port))
        declinecall=QPushButton(self)
        declinecall.setIcon(QIcon("./images/decline.png"))
        declinecall.clicked.connect(lambda:self.declineCall(host,port))
        btnslayout.addWidget(acceptcall)
        btnslayout.addWidget(declinecall)

        pagelayout.addLayout(btnslayout)
        self.calldlg.setLayout(pagelayout)
        self.calldlg.exec()


    def initContacts(self):
        warninglayout=QHBoxLayout()
        self.reloadbtn=QPushButton(self)
        self.NAlbl=QLabel("Sem contatos disponíveis",self)
        self.reloadbtn.setIcon(QIcon("./images/reload.png"))
        self.reloadbtn.clicked.connect(self.reload)
        
        warninglayout.addWidget(self.NAlbl,alignment=Qt.AlignHCenter)
        warninglayout.addWidget(self.reloadbtn,alignment=Qt.AlignHCenter)
        self.pagelayout.addLayout(warninglayout)

        if self.contacts:
            self.NAlbl.hide()
            for c in self.contacts:
                contactlayout=QHBoxLayout()
                label=QLabel(c["nome"],self)
                contactlayout.addWidget(label,alignment=Qt.AlignHCenter)
                btn=QPushButton(self)
                btn.setFixedSize(100,50)
                btn.setIcon(QIcon("./images/accept.png"))
                btn.clicked.connect(lambda:self.invite(c))  
                contactlayout.addWidget(btn,alignment=Qt.AlignHCenter)
                self.pagelayout.addLayout(contactlayout)

    def acceptCall(self,destip,destport):
        self.sendAccept(destip,destport)
        self.showCall(destip,destport)

    def showCall(self,destip,destport):
        self.cw=CallWindow(self,self.hostip,self.hostport+1,destip,destport+1)
        self.cw.show()
        if self.calldlg:
            self.calldlg.close()
        self.hide()

    def declineCall(self,host,port):
        self.sendRefuse(host,port)
        self.calldlg.close()
       
    def invite(self,c):
        self.sendInvite(c)

    def showFailDialog(self):
        self.calldlg = QDialog(self)
        self.calldlg.setWindowTitle("Incoming Call")
        lbl=QLabel("Ligação recusada",self)
        pagelayout=QVBoxLayout()
        pagelayout.addWidget(lbl)
        self.calldlg.setLayout(pagelayout)
        self.calldlg.exec()

    def initSocket(self):
        self.inStream = StreamManager.startStream(isInput=True)
        self.outStream = StreamManager.startStream(isInput=False)
        self.udpSocket = QUdpSocket(self)
        self.udpSocket.bind(QHostAddress(self.hostip), self.hostport)
        self.udpSocket.readyRead.connect(self.readPendingDatagrams)
    
    def readPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            response,host,port= self.udpSocket.readDatagram(1024)
            if response:
                if response.decode('utf-8')=="convite":
                    self.showCallDialog(host.toString(),port)
                elif response.decode('utf-8')=="recusado":
                    self.showFailDialog()
                elif response.decode('utf-8')=="aceito":
                    self.showCall(host.toString(),port)
    
    def sendInvite(self,contact):
        self.udpSocket.writeDatagram("convite".encode('utf-8'),QHostAddress(contact["endIp"]),int(contact["porta"]))
    def sendRefuse(self,host,port):
        self.udpSocket.writeDatagram("recusado".encode('utf-8'),QHostAddress(host),int(port))
    def sendAccept(self,host,port):
        self.udpSocket.writeDatagram("aceito".encode('utf-8'),QHostAddress(host),int(port))