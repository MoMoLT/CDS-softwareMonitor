import sys
import CDSGuiNew
from PyQt5 import QtWidgets, QtGui

if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    app.setWindowIcon(QtGui.QIcon('icon3.png'))
    gui = CDSGuiNew.Gui()
    
    sys.exit(app.exec_())
    