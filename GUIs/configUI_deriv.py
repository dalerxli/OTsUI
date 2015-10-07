from GUIs.configUI_dialog import *
from pyqtgraph import PlotWidget, AxisItem, setConfigOption
from PyQt5.Qt import QStyle, QFileDialog
from PyQt5.QtWidgets import QDialog, QMessageBox
import PyQt5
import configparser as cfg
from os import sep
from libs.usefulVar import nameTypeDict, gettingSettingSignalDict

class configDial(Ui_configDial,QDialog):

    def __init__(self,cfgFile,parent = None):

        super(configDial,self).__init__(parent)
        self.setupUi(self)

        self.parent = parent
        self.parser = cfg.ConfigParser()
        self.parser.read(cfgFile)
        self.cfgFile = cfgFile
        self.paramsDict = {}
        self.fillControls()
        self.fillAxis()


    def fillControls(self):
        secs = self.parser.sections()
        for s in secs:
            self.paramsDict[s] = {}
            options = self.parser.options(s)
            for o in options:
                self.paramsDict[s][o] = [self.parser.get(s,o),None]
        self.ipaddr_Line.setText(self.paramsDict['CONN']['ipaddr'][0])
        self.pubport_Line.setText(self.paramsDict['CONN']['pubport'][0])
        self.subport_Line.setText(self.paramsDict['CONN']['subport'][0])
        self.stimmaxfreq_NumDbl.setValue(float(self.paramsDict['OTHER']['stimmaxfreq'][0]))


    def fillAxis(self):

        axis = self.axisCmbBox.currentText() + 'AXIS'
        try:
            self.disconnect()
        except:
            pass
        self.devname_Line.setText(self.paramsDict[axis]['devname'][0])
        self.vgalvmax_NumDbl.setValue(float(self.paramsDict[axis]['vgalvmax'][0]))
        self.vgalvmin_NumDbl.setValue(float(self.paramsDict[axis]['vgalvmin'][0]))
        self.nmgalvmax_NumDbl.setValue(float(self.paramsDict[axis]['nmgalvmax'][0]))
        self.nmgalvmin_NumDbl.setValue(float(self.paramsDict[axis]['nmgalvmin'][0]))
        self.qpdmax_NumDbl.setValue(float(self.paramsDict[axis]['qpdmax'][0]))
        self.qpdmin_NumDbl.setValue(float(self.paramsDict[axis]['qpdmin'][0]))
        self.pmax_NumDbl.setValue(float(self.paramsDict[axis]['pmax'][0]))
        self.imax_NumDbl.setValue(float(self.paramsDict[axis]['imax'][0]))
        self.speedmax_NumDbl.setValue(float(self.paramsDict[axis]['speedmax'][0]))

        self.speedmax_NumDbl.setEnabled(axis!='ZAXIS')
        self.imax_NumDbl.setEnabled(axis!='YAXIS')

        self.connections()


    def updateParamsDict(self,culprit):

        axis = self.axisCmbBox.currentText() + 'AXIS'
        name = nameTypeDict[type(culprit)]
        funcs = gettingSettingSignalDict[name]
        culpritTag = culprit.objectName().split('_')[0]
        self.paramsDict[axis][culpritTag][0] = str(eval('self.{0}.{1}'.format(culprit.objectName(),funcs[0])))


    def connections(self):

        self.axisCmbBox.currentIndexChanged.connect(self.fillAxis)
        self.ipaddr_Line.textChanged.connect(lambda: self.updateParamsDict(self.ipaddr_Line))
        self.pubport_Line.textChanged.connect(lambda: self.updateParamsDict(self.pubport_Line))
        self.subport_Line.textChanged.connect(lambda: self.updateParamsDict(self.subport_Line))
        self.stimmaxfreq_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.stimmaxfreq_NumDbl))
        self.devname_Line.textChanged.connect(lambda: self.updateParamsDict(self.devname_Line))
        self.vgalvmax_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.vgalvmax_NumDbl))
        self.vgalvmin_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.vgalvmin_NumDbl))
        self.nmgalvmax_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.nmgalvmax_NumDbl))
        self.nmgalvmin_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.nmgalvmin_NumDbl))
        self.qpdmax_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.qpdmax_NumDbl))
        self.qpdmin_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.qpdmin_NumDbl))
        self.pmax_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.pmax_NumDbl))
        self.imax_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.imax_NumDbl))
        self.speedmax_NumDbl.valueChanged.connect(lambda: self.updateParamsDict(self.speedmax_NumDbl))


    def disconnect(self):

        self.axisCmbBox.currentIndexChanged.disconnect()
        self.ipaddr_Line.textChanged.disconnect()
        self.pubport_Line.textChanged.disconnect()
        self.subport_Line.textChanged.disconnect()
        self.stimmaxfreq_NumDbl.valueChanged.disconnect()
        self.devname_Line.textChanged.disconnect()
        self.vgalvmax_NumDbl.valueChanged.disconnect()
        self.vgalvmin_NumDbl.valueChanged.disconnect()
        self.nmgalvmax_NumDbl.valueChanged.disconnect()
        self.nmgalvmin_NumDbl.valueChanged.disconnect()
        self.qpdmax_NumDbl.valueChanged.disconnect()
        self.qpdmin_NumDbl.valueChanged.disconnect()
        self.pmax_NumDbl.valueChanged.disconnect()
        self.imax_NumDbl.valueChanged.disconnect()
        self.speedmax_NumDbl.valueChanged.disconnect()


    def accept(self):

        warningDial = QMessageBox(self)
        warningDial.setWindowTitle('WARNING')
        warningDial.setText('The changes made to the configuration file will become effective the next time you open CoMPlEx ui')
        warningDial.setStandardButtons(QMessageBox.Ok)
        answer = warningDial.exec_()
        super(configDial,self).accept()


    def reject(self):

        print('Bad')
        super(configDial,self).reject()

