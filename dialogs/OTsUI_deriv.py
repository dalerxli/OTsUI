from dialogs.OTsUI_main import *
from tools.guiUtils import *
from pyqtgraph import PlotWidget, AxisItem
from PyQt5.Qt import QStyle
#from PyQt5.Qt import Alignement
class OTsUI(Ui_OTsUI_main):
    
    def setupUi(self,MainWindow):
        super(OTsUI, self).setupUi(MainWindow)
        self.kx = -1
        self.ky = -1
        self.kz = -1
        self.sx = -1
        self.sy = -1
        self.sz = -1
        
        # Setting up the interconnection between UI controls
        
        self.zPNumDbl.valueChanged.connect(self.zPDial.setValue)
        self.zPDial.valueChanged.connect(self.zPNumDbl.setValue)
        
        self.zINumDbl.valueChanged.connect(self.zIDial.setValue)
        self.zIDial.valueChanged.connect(self.zINumDbl.setValue)
        
        self.xyPNumDbl.valueChanged.connect(self.xyPDial.setValue)
        self.xyPDial.valueChanged.connect(self.xyPNumDbl.setValue)
        
        self.xyINumDbl.valueChanged.connect(self.xyIDial.setValue)
        self.xyIDial.valueChanged.connect(self.xyINumDbl.setValue)
        
        self.zOffSetNumDbl.valueChanged.connect(self.zOffSetDial.setValue)
        self.zOffSetDial.valueChanged.connect(self.zOffSetNumDbl.setValue)
        
        self.xOffSetNumDbl.valueChanged.connect(self.xOffSetDial.setValue)
        self.xOffSetDial.valueChanged.connect(self.xOffSetNumDbl.setValue)
        
        self.yOffSetNumDbl.valueChanged.connect(self.yOffSetDial.setValue)
        self.yOffSetDial.valueChanged.connect(self.yOffSetNumDbl.setValue)
        
        self.xSpeedTrapPadSlider.valueChanged.connect(self.xSpeedTrapPadNumDbl.setValue)
        self.xSpeedTrapPadNumDbl.valueChanged.connect(self.xSpeedTrapPadSlider.setValue)
        
        self.ySpeedTrapPadSlider.valueChanged.connect(self.ySpeedTrapPadNumDbl.setValue)
        self.ySpeedTrapPadNumDbl.valueChanged.connect(self.ySpeedTrapPadSlider.setValue)
        
        ######################################
        
        self.sig1Plot = PlotWidget(self.signalTab,background='w')
        self.sig1Plot.setObjectName("sig1Plot")
        self.signalTabGrid.addWidget(self.sig1Plot, 0, 0, 1, 6)
        
        self.sig2Plot = PlotWidget(self.signalTab,background='w')
        self.sig2Plot.setObjectName("sig2Plot")
        self.signalTabGrid.addWidget(self.sig2Plot, 2, 0, 1, 3)
        
        self.sig3Plot = PlotWidget(self.signalTab,background='w')
        self.sig3Plot.setObjectName("sig3Plot")
        self.signalTabGrid.addWidget(self.sig3Plot, 2, 3, 1, 3)
        
        self.powSpec1Plot = PlotWidget(self.signalTab,background='w')
        self.powSpec1Plot.setObjectName("powSpec1Plot")
        self.psTabGrid.addWidget(self.powSpec1Plot, 0, 0, 1, 6)
        
        self.powSpec2Plot = PlotWidget(self.signalTab,background='w')
        self.powSpec2Plot.setObjectName("powSpec2Plot")
        self.psTabGrid.addWidget(self.powSpec2Plot, 2, 0, 1, 3)
        
        self.powSpec3Plot = PlotWidget(self.signalTab,background='w')
        self.powSpec3Plot.setObjectName("powSpec3Plot")
        self.psTabGrid.addWidget(self.powSpec3Plot, 2, 3, 1, 3)
        
        self.trapPadPlot = PlotWidget(self.signalTab,background='w')
        #self.trapPadPlot.plotItem.hideAxis('left')
        #self.trapPadPlot.plotItem.hideAxis('bottom')
        self.trapPadPlot.plotItem.showAxis('top', show=True)
        self.trapPadPlot.plotItem.showAxis('right', show=True)
        self.trapPadPlot.plotItem.showGrid(True, True, 1)
        self.trapPadPlot.setMaximumSize(QtCore.QSize(180, 180))
        self.trapPadPlot.setObjectName("trapPadPlot")
        self.padVert.replaceWidget(self.trpPadPlot,self.trapPadPlot)
        