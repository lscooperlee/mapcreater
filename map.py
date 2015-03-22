
from PySide import QtGui, QtCore

from collections import deque
import math

class RobotMap(QtGui.QImage):

    def __init__(self, width, height):
        super().__init__(width, height, QtGui.QImage.Format_ARGB32)
        self.width=width
        self.height=height

    def draw(self, point, pen):
        self.points.append(point)
        if len(self.points) >= 2:
            pt=QtGui.QPainter(self)
            pt.setPen(pen)
            pt.drawLine(self.points[-2],self.points[-1])

    def erase(self, point, eraser):
        pt=QtGui.QPainter(self)
        eraser.moveTo(point.x()-eraser.width()//2,point.y()-eraser.height()//2)
        pt.eraseRect(eraser)

    def work(self, point, tool):
        if isinstance(tool, QtGui.QPen):
            self.draw(point,tool)
        elif isinstance(tool, QtCore.QRect):
            self.erase(point,tool)

class Map(RobotMap):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.fill(QtCore.Qt.white)
        self.points=deque(maxlen=2)

#        pt=QtGui.QPainter(self)
#        pt.setPen(QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
#        upleft=QtCore.QPoint(0,0)
#        upright=QtCore.QPoint(width, 0)
#        downleft=QtCore.QPoint(0, height)
#        downright=QtCore.QPoint(width, height)
#        pt.drawLine(upleft,upright)
#        pt.drawLine(upleft,downleft)
#        pt.drawLine(downright,upright)
#        pt.drawLine(downright,downleft)



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


    def get_position_list(self, num_point):
        ptlist=[(self.points[0].x(), self.points[0].y())]
        for i in range(len(self.points)-1):
            lf=QtCore.QLineF(self.points[i],self.points[i+1])
            pace=[x/lf.length() for x in range(int(lf.length()))]
            for i in pace:
                p=lf.pointAt(i)
                if ptlist[-1] != (p.x(), p.y()):
                    ptlist.append((p.x(), p.y()))
    
        poslist=[(round(ptlist[0][0]), round(ptlist[0][1]),90)] #the init angle is along y axis, in Qt angle system, it is 90
        for i in range(1, len(ptlist)-1, math.ceil(len(ptlist)/num_point)):
            s=ptlist[i-1]                   
            e=ptlist[i+1]
            s=ptlist[i] if s == e else s    #if s == e, another point is needed, otherwise it will be an zero divide error
            p=(round(s[0]), round(s[1]))    #int points, easy to check repeat, save memory
            d=math.sqrt((s[0]-e[0])**2+(s[1]-e[1])**2)
            arad=math.acos((e[0]-s[0])/d)      #radian, so need to change to Qt angle, x axis is 0, y axis is 90
            a=arad*180/math.pi if e[1]<s[1] else -arad*180/math.pi
            if poslist[-1][:-1] != p:
                poslist.append((p[0],p[1],a))
        
        return poslist

    def get_scan_point(self, pa):
        point_obstacle_list=[]
        point=QtCore.QPointF(pa[0],pa[1])
        angle=pa[2]
        for i in range(180):
            lf=QtCore.QLineF()
            lf.setP1(point)
            lf.setAngle(i-90+angle)            #angle is the direction that the robot faces.
            lf.setLength(self.width+self.height)
            pf=self.__find_overlap(lf)
            point_obstacle_list.append((pf.x(),pf.y()))
            
        return point_obstacle_list

    def __find_overlap(self, linef):
        ql=linef
        pace=[ x/ql.length() for x in range(int(ql.length()))] + [1.0]
        tp=QtGui.QColor(QtCore.Qt.white).rgba()
        for i in pace:
            pf=ql.pointAt(i)
            p=pf.toPoint()
            pp=self.parent.pixel(p)
            if pp != tp:
                return pf

        return None

    def __istaken(self, point):
        ql=QtCore.QLineF(self.points[-1], point)
        if not self.__find_overlap(ql):
            return False
        else:
            return True
