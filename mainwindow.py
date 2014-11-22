
from PySide import QtCore, QtGui

import sys

from ui_mapcreater import Ui_MainWindow
from ui_newmap import Ui_newmap
from mapcanvas import MapCanvas
from map import Map

class MainWindow(QtGui.QMainWindow):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUI__()


    def __initUI__(self):
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        g1=QtGui.QActionGroup(self)
        g1.addAction(self.ui.actionDrawMap)
        g1.addAction(self.ui.actionDrawRoute)

        g2=QtGui.QActionGroup(self)
        g2.addAction(self.ui.actionEraser)
        g2.addAction(self.ui.actionPen)

        self.mc=MapCanvas(self)
        self.setCentralWidget(self.mc)
        

    @QtCore.Slot()
    def on_actionNew_triggered(self):
        nm=QtGui.QDialog()
        nm.ui=Ui_newmap()
        nm.ui.setupUi(nm)
        if nm.exec_() == nm.Accepted:
            width=int(nm.ui.lineEditWidth.text())
            height=int(nm.ui.lineEditHeight.text())
            self.mc.SIG_NEWMAP.emit(width,height)
            self.ui.actionPen.setChecked(True)
            self.ui.actionDrawMap.setChecked(True)


    @QtCore.Slot()
    def on_actionDrawMap_triggered(self):
        self.mc.SIG_DRAWMAP.emit(1)

    @QtCore.Slot()
    def on_actionDrawRoute_triggered(self):
        self.mc.SIG_DRAWROUTE.emit(1)

    @QtCore.Slot()
    def on_actionPen_triggered(self):
        self.mc.SIG_USEPEN.emit(1)

    @QtCore.Slot()
    def on_actionEraser_triggered(self):
        self.mc.SIG_USEERASER.emit(1)
