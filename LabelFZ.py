# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LabelFZ.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LabelFZ(object):
    def setupUi(self, LabelFZ):
        LabelFZ.setObjectName("LabelFZ")
        LabelFZ.resize(853, 825)
        self.centralwidget = QtWidgets.QWidget(LabelFZ)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(63, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 2, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.MplWidget = mplwidget1plot(self.centralwidget)
        self.MplWidget.setMinimumSize(QtCore.QSize(450, 350))
        self.MplWidget.setObjectName("MplWidget")
        self.verticalLayout_3.addWidget(self.MplWidget)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.previousPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.previousPushButton.setObjectName("previousPushButton")
        self.horizontalLayout.addWidget(self.previousPushButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.nextPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextPushButton.setObjectName("nextPushButton")
        self.horizontalLayout.addWidget(self.nextPushButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.idxLabel = QtWidgets.QLabel(self.centralwidget)
        self.idxLabel.setObjectName("idxLabel")
        self.verticalLayout_2.addWidget(self.idxLabel)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 2, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem10)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem11)
        self.loadPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadPushButton.setObjectName("loadPushButton")
        self.verticalLayout.addWidget(self.loadPushButton)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem12)
        self.getPointPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.getPointPushButton.setObjectName("getPointPushButton")
        self.verticalLayout.addWidget(self.getPointPushButton)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem13)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(230, 20))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem14)
        self.exportPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportPushButton.setObjectName("exportPushButton")
        self.verticalLayout.addWidget(self.exportPushButton)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem15)
        self.directoryPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.directoryPushButton.setObjectName("directoryPushButton")
        self.verticalLayout.addWidget(self.directoryPushButton)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem16)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem17)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 3, 2, 2)
        spacerItem18 = QtWidgets.QSpacerItem(62, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem18, 1, 2, 1, 1)
        spacerItem19 = QtWidgets.QSpacerItem(225, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem19, 1, 4, 1, 1)
        LabelFZ.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LabelFZ)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 853, 22))
        self.menubar.setObjectName("menubar")
        LabelFZ.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LabelFZ)
        self.statusbar.setObjectName("statusbar")
        LabelFZ.setStatusBar(self.statusbar)

        self.retranslateUi(LabelFZ)
        QtCore.QMetaObject.connectSlotsByName(LabelFZ)

    def retranslateUi(self, LabelFZ):
        _translate = QtCore.QCoreApplication.translate
        LabelFZ.setWindowTitle(_translate("LabelFZ", "MainWindow"))
        self.previousPushButton.setText(_translate("LabelFZ", "Previous"))
        self.nextPushButton.setText(_translate("LabelFZ", "Next"))
        self.idxLabel.setText(_translate("LabelFZ", "-"))
        self.loadPushButton.setText(_translate("LabelFZ", "Load"))
        self.getPointPushButton.setText(_translate("LabelFZ", "Get Point"))
        self.label.setText(_translate("LabelFZ", "-"))
        self.exportPushButton.setText(_translate("LabelFZ", "Export"))
        self.directoryPushButton.setText(_translate("LabelFZ", "Directory"))
from mplwidget1plot import mplwidget1plot
