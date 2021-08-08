"""
Main functtion for initiatinf the labelFZ application
"""

#from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
#from PyQt5 import QtCore
import sys
#import matplotlib.pyplot as plt
from .local_classes.labelFZ_GUI import *
#from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
#import numpy as np
#from .local_classes.classNanoscopeForceVolume import *
#from .local_classes.classNanoscopeForceRamp import *
#import os



if __name__=="__main__":
    app = QApplication(sys.argv)
    # Creates an instance of the main GUI
    # defined in labelFZ_GUI.py
    w = labelFZ_GUI()
    w.show()
    sys.exit(app.exec_())
