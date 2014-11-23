
from PySide import QtGui, QtCore

from collections import deque


class RobotMap(QtGui.QImage):

    def __init__(self, width, height):
        super().__init__(width, height, QtGui.QImage.Format_ARGB32)

    def draw(self, point, pen):
        self.points.append(point)
        if len(self.points) >= 2:
            pt=QtGui.QPainter(self)
            pt.setPen(pen)
            pt.drawLine(self.points[-2],self.points[-1])

    def erase(self, point, eraseWidth):
        pt=QtGui.QPainter(self)
        eraser=QtCore.QRect(point.x()-eraseWidth//2, point.y()-eraseWidth//2, eraseWidth,eraseWidth)
        pt.eraseRect(eraser)


class Map(RobotMap):

    def __init__(self, width, height, pen):
        super().__init__(width, height)
        self.fill(QtCore.Qt.white)
        self.points=deque(maxlen=2)
        pt=QtGui.QPainter(self)
        pt.setPen(pen)
        upleft=QtCore.QPoint(0,0)
        upright=QtCore.QPoint(width, 0)
        downleft=QtCore.QPoint(0, height)
        downright=QtCore.QPoint(width, height)
        pt.drawLine(upleft,upright)
        pt.drawLine(upleft,downleft)
        pt.drawLine(downright,upright)
        pt.drawLine(downright,downleft)


class Route(RobotMap):

    def __init__(self, parent, width, height):
        super().__init__(width, height)
        self.points=[]
        self.parent=parent

    
    def draw(self, point, pen):
        if len(self.points) == 0:
            self.points.append(point)
            return
        if not self.__istaken(point):
            self.points.append(point)
            pt=QtGui.QPainter(self)
            pt.setPen(pen)
            pt.drawLine(self.points[-2],self.points[-1])

    
    def erase(self, point, eraser):
        pass


    def __istaken(self, point):
        ql=QtCore.QLineF(self.points[-1], point)
        pace=[ x/ql.length() for x in range(int(ql.length()))] + [1]
        tp=QtGui.QColor(QtCore.Qt.white).rgba()
        for i in pace:
            p=ql.pointAt(i).toPoint()
            pp=self.parent.pixel(p)
            if pp != tp:
                return True

        return False

