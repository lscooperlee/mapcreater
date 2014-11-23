

from PySide import QtGui, QtCore
from map import Map, Route

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

        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding); 

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
            self.drawto(e.pos())
            self.update()

    def mouseReleaseEvent(self, e):
        if self.leftpressing == True:
            self.leftpressing = False


    def drawto(self, point):

        if self.drawing == True:
            if self.isdrawingmap == True:
                self.mapimage.draw(point, self.pen)
            else:
                self.routeimage.draw(point, self.pen)
        elif self.drawing == False:        
            if self.isdrawingmap == True:
                self.mapimage.erase(point, self.eraseWidth)
            else:
                self.routeimage.erase(point, self.eraseWidth)


    @QtCore.Slot()
    def createMap(self, width, height):
        self.prepareDrawMap(2)
        self.mapimage=Map(width,height,self.pen)
        self.routeimage=Route(self.mapimage, width, height)

    @QtCore.Slot()
    def prepareDrawMap(self, penWidth):
        self.pen=QtGui.QPen(QtCore.Qt.black, penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.drawing=True
        self.isdrawingmap=True

    @QtCore.Slot()
    def prepareDrawRoute(self, penWidth):
        self.pen=QtGui.QPen(QtCore.Qt.red, penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.drawing=True
        self.isdrawingmap=False

    @QtCore.Slot()
    def prepareUseEraser(self, eraseWidth):
        self.eraseWidth=eraseWidth
        self.drawing=False

    @QtCore.Slot()
    def prepareUsePen(self, penWidth):
        self.pen.setWidth(penWidth)
        self.drawing=True
