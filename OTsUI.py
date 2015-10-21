
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyleFactory

from GUIs.OTsUI_Engine import OTsUI
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainForm = OTsUI()
    mainForm.show()
    
    app.exec_()
    
    print('Work in progress...')