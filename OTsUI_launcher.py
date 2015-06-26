from epz import ch_fw as fw
#from epz import ch_hw as hw
#from epz import epdspic as pic
#from epz import consumer_qt
import sys
import epz.epz3 as epz

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow

from dialogs.OTsUI_deriv import OTsUI

class MainW(QMainWindow, OTsUI):
    def __init__(self, parent=None):
        super(MainW, self).__init__(parent)
        self.setupUi(self)
        
if __name__ == '__main__':
    
#    fw = epz.Forwarder()
#    fw.start()
    
    app = QApplication(sys.argv)
    
    mainForm = MainW()
    mainForm.show()
    
    app.exec_()
    
    print('Work in progress...')
    