from PySide import QtCore, QtGui
import sys
from mainwindow import MainWindow


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
