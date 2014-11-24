
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
        self.defautcursor=self.cursor()


    def __initUI__(self):
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        g1=QtGui.QActionGroup(self)
        g1.addAction(self.ui.actionDrawMap)
        g1.addAction(self.ui.actionDrawRoute)

        g2=QtGui.QActionGroup(self)
        g2.addAction(self.ui.actionEraser)
        g2.addAction(self.ui.actionPen)

        self.sa=QtGui.QScrollArea()
        self.sa.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn);
        self.sa.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn);
        self.sa.setWidgetResizable(False);


        self.mc=MapCanvas(self.sa)
#        self.lo=QtGui.QLayout(self.mc)
        self.sa.setWidget(self.mc)

        self.setCentralWidget(self.sa)
        self.centralWidget().setAlignment(QtCore.Qt.AlignCenter)

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
        self.ui.actionPen.setChecked(True)
        self.mc.setCursor(self.defautcursor)
        self.mc.SIG_DRAWMAP.emit(2)

    @QtCore.Slot()
    def on_actionDrawRoute_triggered(self):
        self.ui.actionPen.setChecked(True)
        self.mc.setCursor(self.defautcursor)
        self.mc.SIG_DRAWROUTE.emit(1)

    @QtCore.Slot()
    def on_actionPen_triggered(self):
        self.mc.setCursor(self.defautcursor)
        self.mc.SIG_USEPEN.emit(2)

    @QtCore.Slot()
    def on_actionEraser_triggered(self):
        pix=QtGui.QPixmap(16,16)
        pix.fill(QtCore.Qt.black)
#        pix.load('res/eraser.png')
        self.mc.setCursor(QtGui.QCursor(pix))
#        self.mc.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
#        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.mc.SIG_USEERASER.emit(16)
