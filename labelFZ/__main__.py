"""
Main function for initiating the labelFZ application
"""

import sys
from .local_classes.labelFZ_GUI import *

if __name__=="__main__":
    app = QApplication(sys.argv)
    # Creates and shows an instance of the main GUI
    # (object of the labelFZ_GUI class)
    # defined in local_classes/labelFZ_GUI.py
    w = labelFZ_GUI()
    w.show()
    sys.exit(app.exec_())
