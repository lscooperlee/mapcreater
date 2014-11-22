

from PySide import QtGui, QtCore
from collections import deque
from map import Map

class MapCanvas(QtGui.QWidget):

    SIG_NEWMAP=QtCore.Signal(int,int)
    SIG_DRAWMAP=QtCore.Signal(int)
    SIG_DRAWROUTE=QtCore.Signal(int)
    SIG_USEERASER=QtCore.Signal(int)
    SIG_USEPEN=QtCore.Signal(int)

    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        self.points=deque(maxlen=2)
        self.leftpressing=False
        self.drawing=None

        self.pen=None
        self.cursor=None
        self.mapimage=None

        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding); 

        self.SIG_NEWMAP.connect(self.createMap)
        self.SIG_DRAWMAP.connect(self.prepareDrawMap)
        self.SIG_DRAWROUTE.connect(self.prepareDrawRoute)
        self.SIG_USEERASER.connect(self.prepareUseEraser)
        self.SIG_USEPEN.connect(self.prepareUsePen)

    def paintEvent(self, e):
        if self.mapimage:
            qp=QtGui.QPainter(self)
            qp.drawImage(e.rect(),self.mapimage,e.rect())

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.points.append(e.pos())                      
            self.leftpressing=True

    def mouseMoveEvent(self, e):
        if self.leftpressing == True:
            self.points.append(e.pos())
            self.drawto(e.pos())
            self.update()

    def mouseReleaseEvent(self, e):
        if self.leftpressing == True:
            self.leftpressing = False

    def drawto(self, point):
        pt=QtGui.QPainter(self.mapimage)

        if self.drawing == True:
            pt.setPen(self.pen)
            pt.drawLine(self.points[-2],self.points[-1])
        elif self.drawing == False:        
            rect=QtCore.QRect(point, QtCore.QSize(20,20))
            pt.eraseRect(rect)


    @QtCore.Slot()
    def createMap(self, width, height):
        self.mapimage=Map(width,height)
        self.prepareDrawMap(1)



    @QtCore.Slot()
    def prepareDrawMap(self, penWidth):
        self.pen=QtGui.QPen(QtCore.Qt.black, penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.drawing=True

    @QtCore.Slot()
    def prepareDrawRoute(self, penWidth):
        self.pen=QtGui.QPen(QtCore.Qt.red, penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.drawing=True

    @QtCore.Slot()
    def prepareUseEraser(self, eraseWidth):
        self.drawing=False

    @QtCore.Slot()
    def prepareUsePen(self, penWidth):
#        self.pen.setPenWidth(penWidth)
        self.drawing=True
