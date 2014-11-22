

from PySide import QtGui, QtCore



class Map(QtGui.QImage):

    def __init__(self, width, height):
        super().__init__(width, height, QtGui.QImage.Format_ARGB32)
        self.fill(QtCore.Qt.white)
