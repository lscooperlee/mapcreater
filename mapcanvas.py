

from PySide import QtGui, QtCore
from map import Map, Route

from collections import namedtuple

class MapCanvas(QtGui.QWidget):

    SIG_NEWMAP=QtCore.Signal(int,int)
    SIG_DRAWMAP=QtCore.Signal(int)
    SIG_DRAWROUTE=QtCore.Signal(int)
    SIG_USEERASER=QtCore.Signal(int)
    SIG_USEPEN=QtCore.Signal(int)

    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        self.leftpressing=False

        self.drawing=None
        self.isdrawingmap=True

        self.pen=None
        self.eraseWidth=None
        self.cursor=None
        self.mapimage=None
        self.routeimage=None

        self.curentTool=None
        self.currentImage=None

        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.SIG_NEWMAP.connect(self.createMap)
        self.SIG_DRAWMAP.connect(self.prepareDrawMap)
        self.SIG_DRAWROUTE.connect(self.prepareDrawRoute)
        self.SIG_USEERASER.connect(self.prepareUseEraser)
        self.SIG_USEPEN.connect(self.prepareUsePen)

    def paintEvent(self, e):
        if self.mapimage and self.routeimage:
            qp=QtGui.QPainter(self)
            qp.drawImage(e.rect(),self.mapimage,e.rect())
            qp.drawImage(e.rect(),self.routeimage,e.rect())

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.leftpressing=True
            self.mapimage.points.append(e.pos())

    def mouseMoveEvent(self, e):
        if self.leftpressing == True:
            self.currentImage.work(e.pos(), self.currentTool)
            self.update()

    def mouseReleaseEvent(self, e):
        if self.leftpressing == True:
            self.leftpressing = False

    def convertMap(self, exporter):
        poslist=self.routeimage.get_position_list(exporter.total_scan)
        print(len(poslist))
        log=exporter.export_info()
        o=exporter.randomise(poslist[0])
        log+=exporter.export_head(0,0,o[2])
        for i in poslist[1:]:
            p=exporter.randomise(i)
            log+=exporter.export_head(o[1]-p[1],p[0]-o[0],p[2])
            olst=self.routeimage.get_scan_point(p)
            olst=[(a[1]-o[1],a[0]-o[0]) for a in olst ]
            log+=exporter.export_scan(olst)
        print(log)

    @QtCore.Slot()
    def createMap(self, width, height):
        self.mapimage=Map(width,height)
        self.routeimage=Route(self.mapimage, width, height)
        self.resize(width, height)

        self.mapimage.pen=QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.routeimage.pen=QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.mapimage.eraser=QtCore.QRect()
        self.routeimage.eraser=QtCore.QRect()


    @QtCore.Slot()
    def prepareDrawMap(self, penWidth):
        self.currentImage=self.mapimage
        self.currentTool=self.currentImage.pen

    @QtCore.Slot()
    def prepareDrawRoute(self, penWidth):
        self.currentImage=self.routeimage
        self.currentTool=self.currentImage.pen

    @QtCore.Slot()
    def prepareUseEraser(self, eraseWidth):
        eraser=self.currentImage.eraser
        eraser.setSize(QtCore.QSize(eraseWidth,eraseWidth))
        self.currentTool=eraser

    @QtCore.Slot()
    def prepareUsePen(self, penWidth):
        pen=self.currentImage.pen
        pen.setWidth(penWidth)
        self.currentTool=pen
