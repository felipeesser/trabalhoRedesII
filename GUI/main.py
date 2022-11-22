import sys
from PyQt5.QtWidgets import *
from entryWindow import EntryWindow
from mainWindow import MainWindow
from PyQt5.QtNetwork import *

def main():
    app=QApplication(sys.argv)
    cl1=EntryWindow('cliente1','127.0.0.1',6666)
    cl1.show()
    cl2=EntryWindow('cliente2','127.0.0.1',7777)
    cl2.show()
    sys.exit(app.exec_())
if __name__=='__main__':
    main()