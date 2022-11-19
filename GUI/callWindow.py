from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from audioStream import *
from PyQt5.QtNetwork import *



class CallWindow(QMainWindow):#https://www.geeksforgeeks.org/pyqt5-how-to-create-circular-image-from-any-image/?tab=article
    def mask_image(self,imgdata, imgtype ='jpg', size = 64):
 
        image = QImage.fromData(imgdata, imgtype)
  
        image.convertToFormat(QImage.Format_ARGB32)
    
        imgsize = min(image.width(), image.height())
        rect = QRect(
            (image.width() - imgsize) // 2,
            (image.height() - imgsize) // 2,
            imgsize,
            imgsize,
        )
        
        image = image.copy(rect)

        out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)
    

        brush = QBrush(image)

        painter = QPainter(out_img)
        painter.setBrush(brush)
   
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(0, 0, imgsize, imgsize)
    
        painter.end()

        pr = QWindow().devicePixelRatio()
        pm = QPixmap.fromImage(out_img)
        pm.setDevicePixelRatio(pr)
        size *= pr
        pm = pm.scaled(int(size), int(size), Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation)

        return pm

    def __init__(self,main,hostip,hostport,destip,destport):
        super(CallWindow,self).__init__()
        self.setWindowTitle("CallWindow")
        self.setGeometry(0, 0, 600, 400)
        self.hostip,self.hostport=hostip,hostport
        self.destip,self.destport=destip,destport
        self.main=main

        self.initSocket()
        
        self.hbox=QHBoxLayout()
        self.profile=QVBoxLayout()
        self.page=QVBoxLayout()

        self.page.addLayout(self.profile)
        self.page.addLayout(self.hbox)

        imgdata = open("./images/profile.jpg", 'rb').read()
        pixmap = self.mask_image(imgdata)

        self.ilabel = QLabel(self)
        self.ilabel.setPixmap(pixmap)
        self.profile.addWidget(self.ilabel,alignment=Qt.AlignHCenter)

        self.tlabel=QLabel(str(self.destport),self)
        self.hbox.addWidget(self.tlabel,alignment=Qt.AlignHCenter)
        self.closecall=QPushButton(self)
        self.closecall.setIcon(QIcon("./images/decline.png"))
        self.closecall.clicked.connect(self.returnWindow)
        self.hbox.addWidget(self.closecall,alignment=Qt.AlignHCenter)


        self.widget=QWidget()
        self.widget.setLayout(self.page)
        self.setCentralWidget(self.widget)
        
    def returnWindow(self):
        self.main.show()
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_S:
            self.writeDatagram()

    def initSocket(self):
        self.main.udpSocket.close()
        self.inStream = StreamManager.startStream(isInput=True)
        self.outStream = StreamManager.startStream(isInput=False)
        self.udpSocket = QUdpSocket(self)
        self.udpSocket.bind(QHostAddress(self.hostip), self.hostport)
        self.udpSocket.readyRead.connect(self.readPendingDatagrams)

    def writeDatagram(self):
        outgoingData = self.inStream.read(StreamManager.CHUNK)
        self.udpSocket.writeDatagram(outgoingData,QHostAddress(self.destip),int(self.destport))

    def readPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            response,host,port= self.udpSocket.readDatagram(StreamManager.CHUNK*2)
            if response:
                self.outStream.write(response)