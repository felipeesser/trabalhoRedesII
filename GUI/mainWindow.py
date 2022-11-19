from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from callWindow import CallWindow
from socket import *
import ast

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("MainWindow")
        self.setGeometry(0, 0, 600, 400)
        self.calldlg=None
        self.pagelayout=QVBoxLayout()
        
        warninglayout=QHBoxLayout()
        self.reloadbtn=QPushButton(self)
        self.reloadbtn.setIcon(QIcon("./images/reload.png"))
        self.reloadbtn.clicked.connect(lambda:self.getAvailableAdresses())
        self.reloadbtn.hide()
        self.NAlbl=QLabel("Sem contatos disponíveis",self)
        self.NAlbl.hide()
        warninglayout.addWidget(self.NAlbl,alignment=Qt.AlignHCenter)
        warninglayout.addWidget(self.reloadbtn,alignment=Qt.AlignHCenter)
        self.pagelayout.addLayout(warninglayout)
        
        self.getAvailableAdresses(0)
        # self.simulateCall()

        self.widget=QWidget()
        self.widget.setLayout(self.pagelayout)
        self.setCentralWidget(self.widget)
        
    def getAvailableAdresses(self):
        #receber contatos disponiveis do servidor de registro.
        # if opt ==1 or opt ==0:
        registerServerSocket = create_connection(('127.0.0.1', 9999))
        registerServerSocket.send('listar_contatos'.encode('utf-8'))
        serverResponse = registerServerSocket.recv(1024).decode('utf-8')
        print('serverResponse: {}'.format(serverResponse))
        contacts = ast.literal_eval(serverResponse.split('resposta, ')[1])
        print('data: {}'.format(contacts))
        self.addresses=contacts
        # else:
        #     addrs=[]
        #     self.addresses=addrs
        self.initContact()
        
    def simulateCall(self):
        #simulacao de ligacao udp
        self.timer = QTimer()
        self.timer.timeout.connect(self.showCallDialog)
        self.timer.start(10000)
            
    def showCallDialog(self, ):
        nome="Maria"
        self.calldlg = QDialog(self)
        self.calldlg.setWindowTitle("Incoming Call")
        pagelayout=QVBoxLayout()
        
        lbl=QLabel("Ligação recebida: "+nome,self)
        pagelayout.addWidget(lbl)
        
        btnslayout=QHBoxLayout()
        acceptcall=QPushButton(self)
        acceptcall.setIcon(QIcon("./images/accept.png"))
        acceptcall.clicked.connect(self.showCall)
        declinecall=QPushButton(self)
        declinecall.setIcon(QIcon("./images/decline.png"))
        declinecall.clicked.connect(self.declineCall)
        btnslayout.addWidget(acceptcall)
        btnslayout.addWidget(declinecall)

        pagelayout.addLayout(btnslayout)
        self.calldlg.setLayout(pagelayout)
        self.calldlg.exec()

        self.timer.stop()#simulacao de ligacao udp

    def initContact(self):

        if self.addresses:
            self.reloadbtn.hide()
            self.NAlbl.hide()
            for a in self.addresses:
                contactlayout=QHBoxLayout()
                label=QLabel(a['nome'],self)
                contactlayout.addWidget(label,alignment=Qt.AlignHCenter)
                btn=QPushButton(self)
                btn.setFixedSize(100,50)
                btn.setIcon(QIcon("./images/accept.png"))
                btn.clicked.connect(self.showCall)  
                contactlayout.addWidget(btn,alignment=Qt.AlignHCenter)
                self.pagelayout.addLayout(contactlayout)
        else:
            self.reloadbtn.show()
            self.NAlbl.show()

    def declineCall(self):
        self.calldlg.close()
    
    def tryContact(self,opt):
        #tenta conexao udp
        if opt:
            return True
        return False
    
    def showCall(self):
        teste=True      #sucesso conexao udp
        #teste=False    #fracasso conexao udp
        if self.tryContact(teste):
            self.call=CallWindow(self)
            self.call.show()
            if self.calldlg:
                self.calldlg.close()
                self.calldlg=None
            self.hide()
        else:
            self.showFailDialog()

    def showFailDialog(self):
        nome="Maria"
        self.calldlg = QDialog(self)
        self.calldlg.setWindowTitle("Incoming Call")
        lbl=QLabel("Ligação recusada: "+nome,self)
        pagelayout=QVBoxLayout()
        pagelayout.addWidget(lbl)
        self.calldlg.setLayout(pagelayout)
        self.calldlg.exec()
