from dialogs.OTsUI_main import *
from tools.guiUtils import *

class OTsUI(OTsUI_main):
    
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