import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import re

class Gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()
    def initGui(self):
        self.setWindowTitle("lineEdit测试")
        
        self.thread = Worker()
        # 垂直布局
        vBoxLayout = QtWidgets.QVBoxLayout(self)
        lt = QtWidgets.QListWidget()
        bt = QtWidgets.QPushButton('开始')
        self.bt = bt
        self.lt = lt
        
        bt.clicked.connect(self.select)
        self.thread.sinOut.connect(self.edit)
        vBoxLayout.addWidget(lt)
        vBoxLayout.addWidget(bt)
        
        
        self.show()
    
    def select(self, index=''):
        #print("activated")
        self.bt.setEnabled(False)
        self.thread.start()
    def edit(self, s):
        #self.line4.setText("在编辑")
        #print("currentIndexChanged")
        self.lt.addItem(s)
    def quitt(self,cb):
        #self.line4.setText("结束编辑")
        print("highlighted")
        print('当前序号',cb.currentIndex())
        print('档期那文本', cb.currentText())
        print(cb.count())

class Worker(QtCore.QThread):
    # 申明一个带str类型参数的信号
    sinOut = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.working = True
        self.num = 0
    def __del__(self):
        #线程状态改变与线程终止
        self.working = False
        self.wait()
    def run(self):
        while self.working == True:
            # 获取文本
            file_str = 'File index{0}'.format(self.num)
            self.num += 1
            # 发射信号
            self.sinOut.emit(file_str)
            # 线程休眠2秒
            self.sleep(2)
'''
255.255.255.255
0-99     \d{2}     
100-199  1\d\d
200-249 2[0-4]\d
250-255 25[0-5]
65536

(1?\d{1,2}|2[0-4]\d|25[0-5]\.){3}(1?\d{1,2}|2[0-4]\d|25[0-5])
'''
def p(a):
    for i in a:
        yield i
if __name__ == '__main__':

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    gui = Gui()
    
    sys.exit(app.exec_())

    '''
    try:
        reIp = '(1?\d{0,2}|2[0-4]\d|25[0-5]\.){3}(1?\d{0,2}|2[0-4]\d|25[0-5])'
        reg = re.compile(reIp)
        a = input().strip()
        ip, port = a.split(':')
        print(ip, port)
        port = int(port)
        if re.match(reg, ip) and 0<= port <= 65535:
            print("正确的ip")
        else:
            print("错误的ip")
    except:
        print("--错误的IP")
    '''
