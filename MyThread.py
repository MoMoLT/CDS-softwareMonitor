from PyQt5 import QtCore

class MyThread(QtCore.QThread):
    sinOut = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.target = None
        self.obj = None
        self.args = None
        
    def __del__(self):
        self.wait()
        
    def run(self):
        
        if self.args:
            status = self.target(*self.args)
            #print("键入这里")
        else:
            status = self.target()
        print('status=',status)
        self.obj.setEnabled(True)
        self.sinOut.emit(status)