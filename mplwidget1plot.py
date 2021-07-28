from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

class mplwidget1plot (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
    
        self.canvas = FigureCanvas(Figure())
        layout = QGridLayout()
        layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot()
        self.setLayout(layout)
