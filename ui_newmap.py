# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_newmap.ui'
#
# Created: Mon Nov 24 02:17:57 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_newmap(object):
    def setupUi(self, newmap):
        newmap.setObjectName("newmap")
        newmap.resize(324, 162)
        self.buttonBox = QtGui.QDialogButtonBox(newmap)
        self.buttonBox.setGeometry(QtCore.QRect(120, 120, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtGui.QWidget(newmap)
        self.widget.setGeometry(QtCore.QRect(90, 40, 191, 51))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.X_2 = QtGui.QLabel(self.widget)
        self.X_2.setObjectName("X_2")
        self.gridLayout.addWidget(self.X_2, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.lineEditWidth = QtGui.QLineEdit(self.widget)
        self.lineEditWidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditWidth.setObjectName("lineEditWidth")
        self.gridLayout.addWidget(self.lineEditWidth, 1, 0, 1, 1)
        self.X = QtGui.QLabel(self.widget)
        self.X.setObjectName("X")
        self.gridLayout.addWidget(self.X, 1, 1, 1, 1)
        self.lineEditHeight = QtGui.QLineEdit(self.widget)
        self.lineEditHeight.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHeight.setObjectName("lineEditHeight")
        self.gridLayout.addWidget(self.lineEditHeight, 1, 2, 1, 1)

        self.retranslateUi(newmap)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), newmap.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), newmap.reject)
        QtCore.QMetaObject.connectSlotsByName(newmap)

    def retranslateUi(self, newmap):
        newmap.setWindowTitle(QtGui.QApplication.translate("newmap", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("newmap", "Width  ", None, QtGui.QApplication.UnicodeUTF8))
        self.X_2.setText(QtGui.QApplication.translate("newmap", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("newmap", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditWidth.setText(QtGui.QApplication.translate("newmap", "800", None, QtGui.QApplication.UnicodeUTF8))
        self.X.setText(QtGui.QApplication.translate("newmap", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditHeight.setText(QtGui.QApplication.translate("newmap", "800", None, QtGui.QApplication.UnicodeUTF8))

