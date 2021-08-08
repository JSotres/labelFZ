from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import QtCore
import sys
import matplotlib.pyplot as plt
from ..qt5_ui_files.LabelFZ import *
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
from .classNanoscopeForceVolume import *
from .classNanoscopeForceRamp import *
import os

class labelFZ_GUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_LabelFZ()
        self.ui.setupUi(self)

        MplToolbar = NavigationToolbar(self.ui.MplWidget.canvas, self)
        self.addToolBar(MplToolbar)

        self.ui.closePushButton.clicked.connect(QApplication.instance().quit)

        
        self.ui.exportPushButton.clicked.connect(self.exportData)
        
        self.ui.actionSetExportDir.triggered.connect(self.selectExportDir)
        self.ui.getPointPushButton.clicked.connect(self.get_point)

        self.ui.nextPushButton.clicked.connect(self.showNextForceRamp)
        self.ui.previousPushButton.clicked.connect(self.showPreviousForceRamp)

        self.ui.actionLoadForceVolume.triggered.connect(self.openForceVolume)
        self.ui.actionLoadForceRamps.triggered.connect(self.openForceRamps)

        self.ui.ForwardDirectionRadioButton.toggled.connect(self.changeFZDirection)
        self.ui.BackwardDirectionRadioButton.toggled.connect(self.changeFZDirection)
        
        self.max_idx=0
        self.min_idx=0
        self.idx=0
        self.y = np.empty([])
        self.x = np.empty([])

        self.xPoint = []
        self.xClass = []

        self.fzDirection = 'ForceForward'
        self.update_graph()        

        self.show()

    def openForceVolume(self):

        self.fzObject = NanoscopeForceVolumeObject()
        self.fzObjectType = "Force Volume"
        self.database_name = 'temporalDataBase.db'
        caption = "Open Nanoscope9 Force Volume File"
        directory = os.getcwd()
        filter_mask = "All Files (*)"
        filenames = QFileDialog.getOpenFileNames(self, caption, directory, filter_mask)[0]
        # Initially, and empty list that will contain the name of the
        # loaded files is created
        self.nameFile = filenames[0]
        self.fzObject.fvToSQL(self.nameFile, self.database_name)
        self.max_idx = self.fzObject.getNumberForceRamps(self.database_name)-1
        self.x, self.y = self.fzObject.getForceRampFromID(self.database_name, self.idx+1, direction=self.fzDirection, xDimensions=False)
        self.ui.idxLabel.setText(str(self.idx))
        self.update_graph()

    def changeFZDirection(self):
        if self.ui.ForwardDirectionRadioButton.isChecked()==True:
            self.fzDirection = 'ForceForward'
            if self.fzObjectType == "Force Volume":
                self.x, self.y = self.fzObject.getForceRampFromID(self.database_name, self.idx+1, direction=self.fzDirection, xDimensions=False)
            else:
                self.y = self.fzObject[self.idx].Ramp[0]['RawY'][0]
        else:
            self.fzDirection = 'ForceBackward'
            if self.fzObjectType == "Force Volume":
                self.x, self.y = self.fzObject.getForceRampFromID(self.database_name, self.idx+1, direction=self.fzDirection, xDimensions=False)
            else:
                self.y = self.fzObject[self.idx].Ramp[0]['RawY'][1]
        self.update_graph()

    def openForceRamps(self):
        self.fzObjectType = "Force Ramps"
        caption = "Open File"
        directory = os.getcwd()
        filter_mask = "All Files (*)"
        self.filenames = QFileDialog.getOpenFileNames(self, caption, directory, filter_mask)[0]
        self.fzObject = []
        self.max_idx = len(self.filenames)-1

        for i in range(len(self.filenames)):
            self.fzObject.append(NanoscopeForceRamp(self.filenames[i]))
            self.fzObject[i].readHeader()
            self.fzObject[i].readRamps()
        if self.fzDirection == 'ForceForward':
            self.y = self.fzObject[self.idx].Ramp[0]['RawY'][0]
        else:
            self.y = self.fzObject[self.idx].Ramp[0]['RawY'][1]
        self.x = np.arange(self.y.shape[0])
        self.ui.idxLabel.setText(str(self.idx))
        self.update_graph()

    def showNextForceRamp(self):

        if self.idx < self.max_idx:
            self.xPoint = []
            self.xClass = []
            self.idx += 1
            self.ui.idxLabel.setText(str(self.idx))
            if self.fzObjectType == "Force Volume":
                self.x, self.y = self.fzObject.getForceRampFromID(self.database_name, self.idx+1, direction=self.fzDirection, xDimensions=False)
            elif self.fzObjectType == "Force Ramps":
                if self.fzDirection == 'ForceForward':
                    self.y = self.fzObject[self.idx].Ramp[0]['RawY'][0]
                else:
                    self.y = self.fzObject[self.idx].Ramp[0]['RawY'][1]
                self.x = np.arange(self.y.shape[0])
            self.update_graph()

    def showPreviousForceRamp(self):

        if self.idx > 0:
            self.xPoint = []
            self.xClass = []
            self.idx -= 1
            self.ui.idxLabel.setText(str(self.idx))
            if self.fzObjectType == "Force Volume":
                self.x, self.y = self.fzObject.getForceRampFromID(self.database_name, self.idx+1, xDimensions=False)
            elif self.fzObjectType == "Force Ramps":
                if self.fzDirection == 'ForceForward':
                    self.y = self.fzObject[self.idx].Ramp[0]['RawY'][0]
                else:
                    self.y = self.fzObject[self.idx].Ramp[0]['RawY'][1]
                self.x = np.arange(self.y.shape[0])
            self.update_graph()

    def get_point(self):
        self.cid = self.ui.MplWidget.canvas.mpl_connect('button_press_event', self.onclick)
        

    def update_graph(self):
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(self.x, self.y)
        if self.xPoint:
            self.ui.MplWidget.canvas.axes.plot(self.xPoint, self.y[np.array(self.xPoint).astype(int)],'ro')
        self.ui.MplWidget.canvas.draw()

    def onclick(self,event):
        #print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata))
        self.ui.MplWidget.canvas.mpl_disconnect(self.cid)
        xpoint=event.xdata
        ypoint=event.ydata
        self.xPoint.append(self.find_nearest(self.x, xpoint))
        self.xPoint.sort()
        
        self.ui.label.setText(str(self.xPoint))

        self.update_graph()

    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def selectExportDir(self):
        self.exportDirectory = QFileDialog.getExistingDirectory(self, "Select Directory to Export Data")

    def exportData(self):
        if self.fzObjectType == "Force Volume":
            q = self.nameFile.split('/')
        elif self.fzObjectType == "Force Ramps":
            q = self.filenames[self.idx].split('/')
                
        #nameFZ = self.exportDirectory + '/file_' + str(self.idx) + '_' + q[-1].split('.')[0] + q[-1].split('.')[1] +'_fz.txt'
        nameFZ = self.exportDirectory + '/' + self.ui.lineEditExportName.text() + '_' + str(self.idx)  + '_fz.txt'
        print(nameFZ)
        np.savetxt(nameFZ, self.y)
        #namePoint = self.exportDirectory + '/file_' + str(self.idx)  + '_' + q[-1].split('.')[0] + q[-1].split('.')[1] + '_labelled_points.txt'
        namePoint = self.exportDirectory + '/' + self.ui.lineEditExportName.text() + '_' + str(self.idx)  +  '_labelled_points.txt'
        print(namePoint)
        np.savetxt(namePoint, self.xPoint)
        
                

if __name__=="__main__":
    app = QApplication(sys.argv)
    # Creates an instance of the main GUI
    # defined in defined in callForceRampGUI.py
    w = labelFZGUI()
    w.show()
    sys.exit(app.exec_())
