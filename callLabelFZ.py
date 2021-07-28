from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import QtCore
import sys
import matplotlib.pyplot as plt
from LabelFZ import *
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
from classNanoscopeForceVolume import *
import os

class labelFZGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LabelFZ()
        self.ui.setupUi(self)

        MplToolbar = NavigationToolbar(self.ui.MplWidget.canvas, self)
        self.addToolBar(MplToolbar)

        
        self.ui.exportPushButton.clicked.connect(self.exportData)
        self.ui.directoryPushButton.clicked.connect(self.selectSaveDirectory)
        self.ui.getPointPushButton.clicked.connect(self.get_point)

        self.ui.nextPushButton.clicked.connect(self.showNextForceRamp)
        self.ui.previousPushButton.clicked.connect(self.showPreviousForceRamp)

        self.ui.loadPushButton.clicked.connect(self.openfiledialog)

        self.fvObject = NanoscopeForceVolumeObject()

        self.database_name = 'temporalDataBase.db'

        
        
        self.max_idx=0
        self.min_idx=0
        self.idx=0
        self.y = np.empty([])
        self.x = np.empty([])

        self.xPoint = []
        self.xClass = []

        self.ui.idxLabel.setText(str(self.idx))
        self.update_graph()

        

        self.show()

    def openfiledialog(self):
        caption = "Open Nanoscope9 Force Volume File"
        directory = os.getcwd()
        filter_mask = "All Files (*)"
        filenames = QFileDialog.getOpenFileNames(self, caption, directory, filter_mask)[0]
        # Initially, and empty list that will contain the name of the
        # loaded files is created
        self.nameFile = filenames[0]
        self.fvObject.fvToSQL(self.nameFile, self.database_name)
        self.max_idx = self.fvObject.getNumberForceRamps(self.database_name)
        self.min_idx = 0
        self.idx = 0
        self.x, self.y = self.fvObject.getForwardForceRampFromID(self.database_name, self.idx+1, xDimensions=False)
        self.update_graph()

    def showNextForceRamp(self):

        if self.idx < self.max_idx:
            self.xPoint = []
            self.xClass = []
            self.idx += 1
            self.ui.idxLabel.setText(str(self.idx))
            self.x, self.y = self.fvObject.getForwardForceRampFromID(self.database_name, self.idx+1, direction='ForceForward', xDimensions=False)
            self.update_graph()

    def showPreviousForceRamp(self):

        if self.idx > 0:
            self.xPoint = []
            self.xClass = []
            self.idx -= 1
            self.ui.idxLabel.setText(str(self.idx))
            self.x, self.y = self.fvObject.getForwardForceRampFromID(self.database_name, self.idx+1, xDimensions=False)
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
        
        self.ui.label.setText(str(self.xPoint))

        self.update_graph()

    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def selectSaveDirectory(self):
        self.saveDirectory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Data")

    def exportData(self):
        nameFZ = self.saveDirectory + '/fz' + str(self.idx) + '.txt'
        np.savetxt(nameFZ, self.y)
        namePoint = self.saveDirectory + '/points' + str(self.idx) + '.txt'
        np.savetxt(namePoint, self.xPoint)

if __name__=="__main__":
    app = QApplication(sys.argv)
    # Creates an instance of the main GUI
    # defined in defined in callForceRampGUI.py
    w = labelFZGUI()
    w.show()
    sys.exit(app.exec_())
