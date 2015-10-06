
import sys

from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow

from GUIs.OTsUI_deriv import OTsUI
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    mainForm = OTsUI()
    mainForm.show()
    
    app.exec_()
    
    print('Work in progress...')
    