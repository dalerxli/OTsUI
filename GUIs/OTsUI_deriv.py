from GUIs.OTsUI_main import *
from pyqtgraph import PlotWidget, AxisItem, setConfigOption
from PyQt5.Qt import QStyle, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import PyQt5
import configparser as cfg
import numpy as np
from os import sep
from os.path import splitext
from GUIs.configUI_deriv import configDial

try:
    import epz as tempEpz
    import inspect
    _,_,keys,_ = inspect.getargspec(tempEpz.CMD.__init__())
    if 'tag' not in keys:
        import libs.epz as tempEpz
    epz = tempEpz
except:
    from libs import epz

setConfigOption('background', 'w')
setConfigOption('foreground', (100,100,100))

INCR = 0.01


class OTsUI(QMainWindow,Ui_OTsUI_main):

    def __init__(self, parent=None):

        super(OTsUI, self).__init__(parent)
        self.setupUi(self)
        self.cfgFile = QFileDialog.getOpenFileName(self,'Select a configuration file',filter='Ini (*.ini)')[0]
        if self.cfgFile == '':
            self.cfgFile = 'config/defaultCfg.ini'
        self.kx = -1
        self.ky = -1
        self.kz = -1
        self.sx = -1
        self.sy = -1
        self.sz = -1
        self.logDir = ''
        self.dataDir = ''
        self.parDir = ''

        # epz objects

        self.otsuiEnv = epz.Environment()

        #######################################################################

        # Plot items
        
        self.trapPadPlot.plotItem.showAxis('top', show=True)
        self.trapPadPlot.plotItem.showAxis('right', show=True)
        self.trapPadPlot.plotItem.showGrid(True, True, 1)
        self.trapPadPlot.setMaximumSize(QtCore.QSize(180, 180))
        
        self.trapPosXYPlot.plotItem.showAxis('top', show=True)
        self.trapPosXYPlot.plotItem.showAxis('right', show=True)
        self.trapPosXYPlot.plotItem.showGrid(True, True, 1)
        self.trapPosXYPlot.setEnabled(True)
        
        self.trapPosZPlot.plotItem.hideAxis('left')
        self.trapPosZPlot.plotItem.showAxis('right', show=True)
        
        #######################################################################
        
        # Set num controls

        self.parDict = self.getParamsDict()
        self.applyConfig()
        
        #for i in range(len(ctrls)):
            #self.configNum(ctrls[i], cfgCtrls[i], cfgKeys[i])
            
        #################################################################################

        self.numConnections()
        self.cmbBoxConnections()
        self.pathConnections()
        self.actionConnections()


    def createConfigDict(self,parser):
        paramsDict = {}
        secs = parser.sections()
        for s in secs:
            paramsDict[s] = {}
            options = parser.options(s)
            for o in options:
                paramsDict[s][o] = parser.get(s,o)

        return paramsDict


    def applyConfig(self):

        parser = cfg.ConfigParser()
        parser.read(self.cfgFile)
        configDict = self.createConfigDict(parser)

        configGroupDictX = {'nmgalvmax': [[self.activeCalXAmplNumDbl], ['nmgalvmin']],
                            'qpdmax': [[self.stdExpXSetPntNumDbl,
                                        self.customExpXAmplNumDbl], ['qpdmin']],
                            'pmax': [[self.xyPNumDbl, self.xyPDial], ['0']],
                            'imax': [[self.xyINumDbl, self.xyIDial], ['0']],
                            'speedmax': [[self.xSpeedTrapPadNumDbl,
                                          self.xSpeedTrapPadSlider], ['INCR']]}
        configGroupDictY = {'nmgalvmax': [[self.activeCalYAmplNumDbl], ['nmgalvmin']],
                            'qpdmax': [[self.stdExpYSetPntNumDbl,
                                        self.customExpYAmplNumDbl], ['qpdmin']],
                            'pmax': [[self.xyPNumDbl, self.xyPDial], ['0']],
                            'imax': [[self.xyINumDbl, self.xyIDial], ['0']],
                            'speedmax': [[self.ySpeedTrapPadNumDbl,
                                          self.ySpeedTrapPadSlider], ['INCR']]}
        configGroupDictZ = {'nmgalvmax': [[self.activeCalZAmplNumDbl], ['nmgalvmin']],
                            'qpdmax': [[self.stdExpZSetPntNumDbl,
                                        self.customExpZAmplNumDbl], ['qpdmin']],
                            'pmax': [[self.zPNumDbl, self.zPDial], ['0']],
                            'imax': [[self.zINumDbl, self.zIDial], ['0']], }
        otherGroupDict = {'stimmaxfreq': [[self.activeCalXFreqNumDbl,self.activeCalYFreqNumDbl,
                                           self.activeCalZFreqNumDbl],['0']]}
        configNumDict = {'XAXIS':configGroupDictX, 'YAXIS':configGroupDictY,
                         'ZAXIS':configGroupDictZ, 'OTHER':otherGroupDict}

        self.ipAddLine.setText(configDict['CONN']['ipaddr'])
        self.subPortLine.setText(configDict['CONN']['subport'])
        self.pubPortLine.setText(configDict['CONN']['pubport'])
        self.xDevName = configDict['XAXIS']['devname']
        self.yDevName = configDict['YAXIS']['devname']
        self.zDevName = configDict['ZAXIS']['devname']

        for s in configNumDict.keys():
            for o in configNumDict[s].keys():
                for el in configNumDict[s][o][0]:
                    scale = (1/INCR) if (type(el) == PyQt5.QtWidgets.QDial or type(el) == PyQt5.QtWidgets.QSlider) else 1
                    max = float(configDict[s][o])
                    minKey = configNumDict[s][o][1][0]
                    min = float(configDict[s][minKey]) if (minKey != '0' and minKey != 'INCR') else eval(minKey)
                    el.setMaximum(max*scale)
                    el.setMinimum(min*scale)
                    el.setSingleStep(INCR*scale)


    def getParamsDict(self):

        baseDict = {PyQt5.QtWidgets.QSpinBox:['NUM','.value()','.setValue(',[]],PyQt5.QtWidgets.QDoubleSpinBox:['DBL','.value()','.setValue(',[]],
                    PyQt5.QtWidgets.QLineEdit:['LINE','.text()','.setText(',[]],PyQt5.QtWidgets.QCheckBox:['CKBOX','.isChecked()','.setChecked(',[]],
                    PyQt5.QtWidgets.QComboBox:['CMBBOX','.currentIndex()','.setCurrentIndex(',[]]}

        for d in dir(self):
            dObj = getattr(self, d)
            try:
                if dObj.isReadOnly():
                    continue
            except:
                pass
            if type(dObj) in baseDict.keys():
                baseDict[type(dObj)][3].append(d)
            else:
                pass

        return baseDict


    def saveParams(self):

        parFileName = str(QFileDialog.getSaveFileName(self,'Choose a name for you parameters file',filter='Parameters Files (*.par)')[0])
        if parFileName == '':
            return None
        splitName = splitext(parFileName)
        if splitName[1] != '.par':
            parFileName = splitName[0]+'.par'

        sDict = self.getParamsDict()
        paramsFile = open(parFileName,'w')
        paramsParser = cfg.ConfigParser()

        paramsParser.add_section('MISC')
        paramsParser.set('MISC','ot',self.cfgFile)
        for k in sDict.keys():
            paramsParser.add_section(sDict[k][0])
            for i in range(len(sDict[k][3])):
                paramsParser.set(sDict[k][0], sDict[k][3][i], str(eval('self.'+sDict[k][3][i]+sDict[k][1])))

        paramsParser.write(paramsFile)
        paramsFile.close()


    def loadParams(self):

        self.cmbBoxDisconnect()
        parFileName = str(QFileDialog.getOpenFileName(self,'Choose a parameters file',filter='Parameters Files (*.par)')[0])
        if parFileName == '':
            return None
        lDict = self.getParamsDict()
        #paramsFile = open(parFileName,'r')
        paramsParser = cfg.ConfigParser()
        paramsParser.read(parFileName)
        print(paramsParser.sections())
        if paramsParser.get('MISC', 'ot') != self.cfgFile:
            warning = QMessageBox(self)
            warning.setText('You tried to load parameters that have been saved for another OT\n'+
                            'Please choose a parameter file for you current OT')
            warning.exec_()
            self.loadParams()
        attrList = dir(self)
        for a in attrList:
            for k in lDict.keys():
                if a in lDict[k][3]:
                    value = paramsParser.get(lDict[k][0],a.lower())
                    try:
                        value = str(eval(value))
                    except:
                        value = '\'' + value + '\''
                    eval('self.' + a + lDict[k][2] + value + ')')
        self.cmbBoxConnections()


    def configNum(self,numName,cfgName,cfgKey):
        
        culprit = getattr(self, numName)
        scale = (1/INCR) if (type(culprit) == PyQt5.QtWidgets.QDial or type(culprit) == PyQt5.QtWidgets.QSlider) else 1
        getattr(self, numName).setMaximum(float(self.cfgParse[cfgKey][cfgName+'MAX'])*scale)
        getattr(self, numName).setMinimum(float(self.cfgParse[cfgKey][cfgName+'MIN'])*scale)
        getattr(self, numName).setSingleStep(INCR*scale)
        getattr(self, numName).setValue(float(self.cfgParse[cfgKey][cfgName])*scale)
        
    
    def changeCmbGrMem(self):
        sendCmb = self.sender()
        fatherCmb = sendCmb.parentWidget()
        listCmbChild = [c for c in fatherCmb.children() if (type(c)==PyQt5.QtWidgets.QComboBox and c is not sendCmb)]
        equalValCmb = [l for l in listCmbChild if l.currentIndex()==sendCmb.currentIndex()][0]
        elements = list(range(sendCmb.count()))
        elements.remove(sendCmb.currentIndex())
        listOtherChild = [c for c in listCmbChild if c is not equalValCmb]
        for c in listOtherChild:
            elements.remove(c.currentIndex())
        equalValCmb.blockSignals(True)
        equalValCmb.setCurrentIndex(elements[0])
        equalValCmb.blockSignals(False)
        
    
    def setScaledValue(self,rec):
        culprit = self.sender()
        scale = rec.singleStep() if (type(culprit) == PyQt5.QtWidgets.QDial or type(culprit) == PyQt5.QtWidgets.QSlider) else 1/culprit.singleStep()
        rec.blockSignals(True)
        rec.setValue(culprit.value()*scale)
        rec.blockSignals(False)
        
        
    def selectDir(self,displayLine):
        
        displayLine.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")))
        
    
    def updateDirObj(self,dir):
        
        culprit = self.sender()
        dir = culprit.text()
        dir=dir.replace('/',sep)


    def showDial(self):

        culprit = self.sender()

        if culprit is self.action_Config_File:
            self.cfgDial = configDial(self.cfgFile,self)
            self.cfgDial.exec_()


    def numConnections(self):

        # Setting up the interconnection between UI numeric controls

        self.zPNumDbl.valueChanged.connect(lambda: self.setScaledValue(self.zPDial))
        self.zPDial.valueChanged.connect(lambda: self.setScaledValue(self.zPNumDbl))

        self.zINumDbl.valueChanged.connect(lambda: self.setScaledValue(self.zIDial))
        self.zIDial.valueChanged.connect(lambda: self.setScaledValue(self.zINumDbl))

        self.xyPNumDbl.valueChanged.connect(lambda: self.setScaledValue(self.xyPDial))
        self.xyPDial.valueChanged.connect(lambda: self.setScaledValue(self.xyPNumDbl))

        self.xyINumDbl.valueChanged.connect(lambda: self.setScaledValue(self.xyIDial))
        self.xyIDial.valueChanged.connect(lambda: self.setScaledValue(self.xyINumDbl))

        self.zOffSetNumDbl.valueChanged.connect(lambda: self.setScaledValue(self.zOffSetDial))
        self.zOffSetDial.valueChanged.connect(lambda: self.setScaledValue(self.zOffSetNumDbl))

        self.xOffSetNumDbl.valueChanged.connect(lambda: self.setScaledValue(self.xOffSetDial))
        self.xOffSetDial.valueChanged.connect(lambda: self.setScaledValue(self.xOffSetNumDbl))

        self.yOffSetNumDbl.valueChanged.connect(lambda: self.setScaledValue(self.yOffSetDial))
        self.yOffSetDial.valueChanged.connect(lambda: self.setScaledValue(self.yOffSetNumDbl))

        self.xSpeedTrapPadSlider.valueChanged.connect(lambda: self.setScaledValue(self.xSpeedTrapPadNumDbl))
        self.xSpeedTrapPadNumDbl.valueChanged.connect(lambda: self.setScaledValue(self.xSpeedTrapPadSlider))

        self.ySpeedTrapPadSlider.valueChanged.connect(lambda: self.setScaledValue(self.ySpeedTrapPadNumDbl))
        self.ySpeedTrapPadNumDbl.valueChanged.connect(lambda: self.setScaledValue(self.ySpeedTrapPadSlider))

        ######################################


    def cmbBoxConnections(self):

        # Setting Plot combo boxes

        self.sig1selCmb.currentIndexChanged.connect(self.changeCmbGrMem)
        self.sig2selCmb.currentIndexChanged.connect(self.changeCmbGrMem)
        self.sig3selCmb.currentIndexChanged.connect(self.changeCmbGrMem)

        self.ps1selCmb.currentIndexChanged.connect(self.changeCmbGrMem)
        self.ps2selCmb.currentIndexChanged.connect(self.changeCmbGrMem)
        self.ps3selCmb.currentIndexChanged.connect(self.changeCmbGrMem)


    def cmbBoxDisconnect(self):

        # Setting Plot combo boxes

        self.sig1selCmb.currentIndexChanged.disconnect()
        self.sig2selCmb.currentIndexChanged.disconnect()
        self.sig3selCmb.currentIndexChanged.disconnect()

        self.ps1selCmb.currentIndexChanged.disconnect()
        self.ps2selCmb.currentIndexChanged.disconnect()
        self.ps3selCmb.currentIndexChanged.disconnect()

        #################################################################################


    def pathConnections(self):

        # Set directories selection

        self.logDirBtn.clicked.connect(lambda: self.selectDir(self.logDirLine))
        self.dataDirBtn.clicked.connect(lambda: self.selectDir(self.dataDirLine))
        self.logDirLine.textChanged.connect(lambda: self.updateDirObj(self.logDir))
        self.dataDirLine.textChanged.connect(lambda: self.updateDirObj(self.dataDir))

        #################################################################################


    def actionConnections(self):

        self.action_Config_File.triggered.connect(self.showDial)
        self.action_Save_Parameters.triggered.connect(self.saveParams)
        self.action_Load_Parameters.triggered.connect(self.loadParams)

        
    