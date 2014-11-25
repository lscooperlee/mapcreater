
from PySide import QtCore, QtGui

import sys

from ui_mapcreater import Ui_mapcreater
from ui_newmap import Ui_newmap
from ui_export import Ui_export
from mapcanvas import MapCanvas
from export import MapExporter

class MainWindow(QtGui.QMainWindow):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUI__()
        self.defautcursor=self.cursor()


    def __initUI__(self):
        self.ui=Ui_mapcreater()
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

            self.on_actionDrawMap_triggered()
            self.on_actionPen_triggered()

            self.ui.actionPen.setChecked(True)
            self.ui.actionDrawMap.setChecked(True)


    
    @QtCore.Slot()
    def on_actionExport_triggered(self):
        nm=QtGui.QDialog()
        nm.ui=Ui_export()
        nm.ui.setupUi(nm)
        if nm.exec_() == nm.Accepted:
            noise_rate=nm.ui.noise_rate_slider.value()/100
            ang_noise_dir=nm.ui.ang_noise_dir_slider.value()/100
            dist_noise_dir=nm.ui.dist_noise_dir_slider.value()/100
            dist_ratio=int(nm.ui.dist_ratio_lineedit.text())
            total_scan=int(nm.ui.total_scan_lineedit.text())

            map_exporter=MapExporter(noise_rate, ang_noise_dir, dist_noise_dir,dist_ratio, total_scan)
            self.mc.convertMap(map_exporter)
#            map_exporter.export('filename')
    

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
        self.mc.setCursor(QtGui.QCursor(pix))
        self.mc.SIG_USEERASER.emit(16)
