from GUIs.OTsUI_MainGUI import *
from pyqtgraph import setConfigOption
from PyQt5.Qt import QFileDialog
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import PyQt5
import configparser as cfg
import numpy as np
from scipy.signal import welch
from os import sep
from os.path import splitext
from GUIs.OTsUI_configUI_Engine import configDial

try:
    import epz as tempEpz
    import inspect
    _,_,keys,_ = inspect.getargspec(tempEpz.CMD.__init__())
    if 'tag' not in keys:
        import libs.epz as tempEpz
    epz = tempEpz
except:
    from libs import epz

from libs.otsui2epz import Interpreter
from libs.usefulVar import pens

setConfigOption('background', 'w')
setConfigOption('foreground', (100,100,100))

INCR = 0.01

DEC = 100
CHUNK = 1000
NOTLEN = 1000


class OTsUI(QMainWindow,Ui_OTsUI_main):

    def __init__(self, parent=None):

        super(OTsUI, self).__init__(parent)
        self.setupUi(self)
        self.cfgFile = QFileDialog.getOpenFileName(self,'Select a configuration file',filter='Ini (*.ini)')[0]
        if self.cfgFile == '':
            self.cfgFile = 'config/defaultCfg.ini'
        self.kx = 1
        self.ky = 1
        self.kz = 1
        self.sx = 1
        self.sy = 1
        self.sz = 1
        self.logDir = ''
        self.dataDir = ''
        self.parDir = ''
        self.xData = None

        self.powSpecConnected = False
        self.signalConnected = False

        self.c = 0

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
        self.buttonConnections()


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

        self.xVToNm = lambda x: ((x-configDict['XAXIS']['vgalvmin'])/(configDict['XAXIS']['vgalvmax']-configDict['XAXIS']['vgalvmin']))*(configDict['XAXIS']['nmgalvmax']-configDict['XAXIS']['nmgalvmin'])+configDict['XAXIS']['nmgalvmin']
        self.xNmToV = lambda x: ((x-configDict['XAXIS']['nmgalvmin'])/(configDict['XAXIS']['nmgalvmax']-configDict['XAXIS']['nmgalvmin']))*(configDict['XAXIS']['vgalvmax']-configDict['XAXIS']['vgalvmin'])+configDict['XAXIS']['vgalvmin']
        self.yVToNm = lambda x: ((x-configDict['YAXIS']['vgalvmin'])/(configDict['YAXIS']['vgalvmax']-configDict['YAXIS']['vgalvmin']))*(configDict['YAXIS']['nmgalvmax']-configDict['YAXIS']['nmgalvmin'])+configDict['YAXIS']['nmgalvmin']
        self.yNmToV = lambda x: ((x-configDict['YAXIS']['nmgalvmin'])/(configDict['YAXIS']['nmgalvmax']-configDict['YAXIS']['nmgalvmin']))*(configDict['YAXIS']['vgalvmax']-configDict['YAXIS']['vgalvmin'])+configDict['YAXIS']['vgalvmin']
        self.XVToNm = lambda x: ((x-configDict['ZAXIS']['vgalvmin'])/(configDict['ZAXIS']['vgalvmax']-configDict['ZAXIS']['vgalvmin']))*(configDict['ZAXIS']['nmgalvmax']-configDict['ZAXIS']['nmgalvmin'])+configDict['ZAXIS']['nmgalvmin']
        self.zNmToV = lambda x: ((x-configDict['ZAXIS']['nmgalvmin'])/(configDict['ZAXIS']['nmgalvmax']-configDict['ZAXIS']['nmgalvmin']))*(configDict['ZAXIS']['vgalvmax']-configDict['ZAXIS']['vgalvmin'])+configDict['ZAXIS']['vgalvmin']

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


    def epzConnect(self):

        self.xInterpreter = Interpreter(self.otsuiEnv,self.xDevName)
        self.yInterpreter = Interpreter(self.otsuiEnv,self.yDevName)
        self.zInterpreter = Interpreter(self.otsuiEnv,self.zDevName)

        self.xData = epz.QtDATA(self.otsuiEnv,self.xDevName)
        self.xData.decimate = DEC
        self.xData.chunk = CHUNK
        self.xData.notifyLength = NOTLEN
        self.xData.notify = True
        self.xData.yDataReceived.connect(self.trapTrack)
        self.xData = epz.QtDATA(self.otsuiEnv,self.yDevName)
        self.yData.decimate = DEC
        self.yData.chunk = CHUNK
        self.yData.notifyLength = NOTLEN
        self.yData.notify = True
        self.yData.yDataReceived.connect(self.trapTrack)
        self.zData = epz.QtDATA(self.otsuiEnv,self.zDevName)
        self.zData.decimate = DEC
        self.zData.chunk = CHUNK
        self.zData.notifyLength = NOTLEN
        self.zData.notify = True
        self.zData.yDataReceived.connect(self.trapTrack)


    def startEpz(self):

        self.xInterpreter.startDev()
        self.yInterpreter.startDev()
        self.zInterpreter.startDev()

        self.xData.start()
        self.yData.start()
        self.zData.start()

        self.linkPlotToData(self.plotTabs.currentIndex()==0)


    def linkPlotToData(self, goSignal):

        signals = [self.xData,self.yData,self.zData]
        if goSignal:
            if self.powSpecConnected or self.signalConnected:
                for s in signals:
                    s.chunkReceived.disconnect()
            signals[self.sig1selCmb.currentIndex()].chunkReceived.connect(self.sig1Update)
            signals[self.sig2selCmb.currentIndex()].chunkReceived.connect(self.sig2Update)
            signals[self.sig3selCmb.currentIndex()].chunkReceived.connect(self.sig3Update)
            self.signalConnected = True
        else:
            if self.powSpecConnected or self.signalConnected:
                for s in signals:
                    s.chunkReceived.disconnect()
            signals[self.ps1selCmb.currentIndex()].chunkReceived.connect(self.ps1Update)
            signals[self.ps2selCmb.currentIndex()].chunkReceived.connect(self.ps2Update)
            signals[self.ps3selCmb.currentIndex()].chunkReceived.connect(self.ps3Update)
            self.powSpecConnected = True


    def sig1Update(self,v):

        self.sig1Plot.plotItem.clear()
        S = list([self.sx,self.sy,self.sz])[self.sig1selCmb.currentIndex()]
        k = list([self.kx,self.ky,self.kz])[self.sig1selCmb.currentIndex()]
        plottableY = np.array(v[1])*S*k
        plottableX = np.array(v[0])-v[0][0]
        self.sig1Plot.plotItem.plot(plottableX,plottableY,pen=pens[0])


    def sig2Update(self,v):

        self.sig2Plot.plotItem.clear()
        S = list([self.sx,self.sy,self.sz])[self.sig2selCmb.currentIndex()]
        k = list([self.kx,self.ky,self.kz])[self.sig2selCmb.currentIndex()]
        plottableY = np.array(v[1])*S*k
        plottableX = np.array(v[0])-v[0][0]
        self.sig1P2ot.plotItem.plot(plottableX,plottableY,pen=pens[1])


    def sig3Update(self,v):

        self.sig3Plot.plotItem.clear()
        S = list([self.sx,self.sy,self.sz])[self.sig3selCmb.currentIndex()]
        k = list([self.kx,self.ky,self.kz])[self.sig3selCmb.currentIndex()]
        plottableY = np.array(v[1])*S*k
        plottableX = np.array(v[0])-v[0][0]
        self.sig3Plot.plotItem.plot(plottableX,plottableY,pen=pens[2])


    def ps1Update(self,v):

        self.powSpec1Plot.plotItem.clear()
        S = list([self.sx,self.sy,self.sz])[self.ps1selCmb.currentIndex()]
        k = list([self.kx,self.ky,self.kz])[self.ps1selCmb.currentIndex()]
        tempY = np.array(v[1])*S*k
        sampF = 1.0/np.mean(np.array(v[0])[1:]-np.array(v[0])[:-1])
        plottableX,plottableY = welch(tempY,sampF)
        self.powSpec1Plot.plotItem.plot(plottableX,plottableY,pen=pens[0])


    def ps2Update(self,v):

        self.powSpec2Plot.plotItem.clear()
        S = list([self.sx,self.sy,self.sz])[self.ps2selCmb.currentIndex()]
        k = list([self.kx,self.ky,self.kz])[self.ps2selCmb.currentIndex()]
        tempY = np.array(v[1])*S*k
        sampF = 1.0/np.mean(np.array(v[0])[1:]-np.array(v[0])[:-1])
        plottableX,plottableY = welch(tempY,sampF)
        self.powSpec2Plot.plotItem.plot(plottableX,plottableY,pen=pens[1])


    def ps3Update(self,v):

        self.powSpec3Plot.plotItem.clear()
        S = list([self.sx,self.sy,self.sz])[self.ps3selCmb.currentIndex()]
        k = list([self.kx,self.ky,self.kz])[self.ps3selCmb.currentIndex()]
        tempY = np.array(v[1])*S*k
        sampF = 1.0/np.mean(np.array(v[0])[1:]-np.array(v[0])[:-1])
        plottableX,plottableY = welch(tempY,sampF)
        self.powSpec3Plot.plotItem.plot(plottableX,plottableY,pen=pens[0])


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

        if self.xData != None:
            self.linkPlotToData((sendCmb is self.sig1selCmb or sendCmb is self.sig1selCmb or sendCmb is self.sig1selCmb))
        
    
    def setScaledValue(self,rec):
        culprit = self.sender()
        scale = rec.singleStep() if (type(culprit) == PyQt5.QtWidgets.QDial or type(culprit) == PyQt5.QtWidgets.QSlider) else 1/culprit.singleStep()
        rec.blockSignals(True)
        rec.setValue(culprit.value()*scale)
        rec.blockSignals(False)
        
        
    def selectDir(self,displayLine):
        
        displayLine.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")))
        
    
    def updateDirObj(self):
        
        culprit = self.sender()
        folder = culprit.text()
        folder=folder.replace('/',sep)
        if culprit == self.logDirLine:
            self.logDir = folder
        else:
            self.dataDir = folder



    def showDial(self):

        culprit = self.sender()

        if culprit is self.action_Config_File:
            self.cfgDial = configDial(self.cfgFile,self)
            self.cfgDial.exec_()


    def closeEvent(self, event):
        print('logdir: '+self.logDir)
        reply = QMessageBox.question(self, 'Message',
            "Do you really want to close OTsUI?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.xData is None:
                event.accept()
                return None
            self.xInterpreter.stopDev()
            self.yInterpreter.stopDev()
            self.zInterpreter.stopDev()

            reply = QMessageBox.question(self, 'Message',
                                               "Do you want to kill the devices (If you say yes, you'll have to turn the towers off and then on before using CoMPlEx again)?",
                                               QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.xInterpreter.killDev()
                self.yInterpreter.killDev()
                self.zInterpreter.killDev()
                self.xyCmd.send('K')

            event.accept()
        else:
            event.ignore()


    def count(self):

        while self.yPlusTrapBtn.isDown():
            self.c+=1
            print(self.c)


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
        self.logDirLine.textChanged.connect(self.updateDirObj)
        self.dataDirLine.textChanged.connect(self.updateDirObj)

        #################################################################################


    def actionConnections(self):

        self.action_Config_File.triggered.connect(self.showDial)
        self.action_Save_Parameters.triggered.connect(self.saveParams)
        self.action_Load_Parameters.triggered.connect(self.loadParams)
        self.action_Exit.triggered.connect(self.close)


    def buttonConnections(self):

        self.yPlusTrapBtn.pressed.connect(self.count)

        
    