QTFILE = open('GUIs/OTsUI_MainGUI.py','r')
for l in QTFILE.readlines():
    if l.find('from PyQt4') != -1:
        ENV = 'PyQt4'
    elif l.find('from PyQt5') != -1:
        ENV = 'PyQt5'
QTFILE.close()

import sys

if ENV == 'PyQt5':
    try:
        from PyQt5.QtWidgets import QApplication
    except:
        print('To use this software you need {0}'.format(ENV))
elif ENV == 'PyQt4':
    try:
        from PyQt4.QtGui import QApplication
    except:
        print('To use this software you need {0}'.format(ENV))

from GUIs.OTsUI_MainGUI_Engine import OTsUI

try:
    VERBOSE = sys.argv[1] == '-v' or sys.argv[1] == '--verbose'
except:
    VERBOSE = False

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainForm = OTsUI()
    mainForm.show()
    
    app.exec_()
    
    print('Work in progress...')