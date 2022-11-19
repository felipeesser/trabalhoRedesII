from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from callManager import CallManager

CALLER=['maria','192.168.0.101','3000']

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

    def __init__(self,main,port):
        
        super(CallWindow,self).__init__()
        self.callManager = CallManager(port)
        self.setWindowTitle("CallWindow")
        self.setGeometry(0, 0, 600, 400)
        self.main=main

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

        self.tlabel=QLabel(CALLER[0],self)
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