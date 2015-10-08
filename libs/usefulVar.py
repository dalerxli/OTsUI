from PyQt5.QtWidgets import *

nameTypeDict = {QLabel:'Label',
                QSpinBox:'Num',
                QDoubleSpinBox:'NumDbl',
                QDial:'Dial',
                QComboBox:'CmbBox',
                QLineEdit:'Line'}

gettingSettingSignalDict = {'Line': ['text()','setText(str(\'','textChanged'],
                            'Num': ['value()','setValue(int(\'','valueChanged'],
                            'NumDbl': ['value()','setValue(float(\'','valueChanged']}

pens = [{'color':'#0033CC','width':1},{'color':'#FF0000','width':1},{'color':'#009900','width':1},
            {'color':'#9933FF','width':1},{'color':'#996600','width':1},{'color':'#660033','width':1},
            {'color':'#000000','width':1},{'color':'#8D9494','width':1}]
