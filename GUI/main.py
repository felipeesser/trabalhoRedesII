import sys
from PyQt5.QtWidgets import *
from entryWindow import EntryWindow

def main():
    app=QApplication(sys.argv)
    gui= EntryWindow()
    gui.show()
    sys.exit(app.exec_())
if __name__=='__main__':
    main()