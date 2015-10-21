from GUIs.OTsUI_configUI_Dialog import *
from PyQt5.Qt import QStyle, QFileDialog
from PyQt5.QtWidgets import QDialog, QMessageBox
import configparser as cfg
from os.path import splitext
from libs.usefulVar import nameTypeDict, gettingSettingSignalDict

NAMES = ['Num','NumDbl','Line']

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
                self.paramsDict[s][o] = self.parser.get(s,o)
        self.ipaddr_Line.setText(self.paramsDict['CONN']['ipaddr'])
        self.pubport_Line.setText(self.paramsDict['CONN']['pubport'])
        self.subport_Line.setText(self.paramsDict['CONN']['subport'])
        self.stimmaxfreq_NumDbl.setValue(float(self.paramsDict['OTHER']['stimmaxfreq']))


    def fillAxis(self):

        axis = self.axisCmbBox.currentText() + 'AXIS'
        try:
            self.disconnect()
        except:
            pass
        for k in self.paramsDict[axis].keys():
            for n in NAMES:
                if k+'_'+n in dir(self):
                    eval('self.{0}.{1}{2}\'))'.format((k+'_'+n),gettingSettingSignalDict[n][1],self.paramsDict[axis][k]))

        self.speedmax_NumDbl.setEnabled(axis!='ZAXIS')
        self.imax_NumDbl.setEnabled(axis!='YAXIS')
        self.pmax_NumDbl.setEnabled(axis!='YAXIS')

        self.connections()


    def updateParamsDict(self,culprit):

        axis = self.axisCmbBox.currentText() + 'AXIS'
        name = nameTypeDict[type(culprit)]
        funcs = gettingSettingSignalDict[name]
        culpritTag = culprit.objectName().split('_')[0]
        self.paramsDict[axis][culpritTag] = str(eval('self.{0}.{1}'.format(culprit.objectName(),funcs[0])))
        if axis == 'XAXIS' and (culpritTag == 'pmax' or culpritTag == 'imax'):
            self.paramsDict['YAXIS'][culpritTag] = self.paramsDict[axis][culpritTag]


    def buildSignal(self,name):

        for n in NAMES:
            if name+'_'+n in dir(self):
                control = 'self.{0}_{1}'.format(name,n)
                return control,'.'+gettingSettingSignalDict[n][2]


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

        for s in ['CONN','OTHER','XAXIS']:
            for o in self.paramsDict[s].keys():
                ctrl,sig = self.buildSignal(o)
                eval(ctrl+sig+'.disconnect()')


    def saveParams(self):

        for s in self.paramsDict.keys():
            for o in self.paramsDict[s].keys():
                self.parser.set(s,o,self.paramsDict[s][o])

        warningDial = QMessageBox(self)
        warningDial.setWindowTitle('Saving...')
        warningDial.setText('Do you want to create a new configuration file?')
        warningDial.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        warningDial.setDefaultButton(QMessageBox.No)
        answer = warningDial.exec_()
        if answer == 65536:
            fp = open(self.cfgFile,'w')
        else:
            fname = str(QFileDialog.getSaveFileName(self,'Choose a name for your new configuration file:',filter='Ini (*.ini)'))
            sf = splitext(fname)
            if sf[1] != '.ini':
                fname = sf[0]+'.ini'
            fp = open(fname,'w')

        self.parser.write(fp)



    def accept(self):

        self.saveParams()

        warningDial = QMessageBox(self)
        warningDial.setWindowTitle('WARNING')
        warningDial.setText('The changes made to the configuration file will become effective the next time you open CoMPlEx ui')
        warningDial.setStandardButtons(QMessageBox.Ok)
        answer = warningDial.exec_()
        super(configDial,self).accept()


    def reject(self):

        print('Bad')
        super(configDial,self).reject()

