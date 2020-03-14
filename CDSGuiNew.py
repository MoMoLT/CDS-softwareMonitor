# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from CDSGui import Ui_MainWindow
import FileSave
import MailSend
import re
from spider import CDSSpider
import MyThread

class Gui(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, title='老梦的禅大师软件监控'):
        super().__init__()
        # 设置线程，监控线程和发邮件线程
        self.tStart = MyThread.MyThread()
        self.tStart.sinOut.connect(self.startStatus)
        self.tSend = MyThread.MyThread()
        self.tSend.sinOut.connect(self.sendStatus)
        
        self.ipSet = []   # ip集合
        self.title = title              # 窗口标题
        self.spider = CDSSpider()       # 一个爬虫
        self.SHOWHEAD = ['APP', '发行商', '类别', '发布时间', '下架时间']
        self.initGui()
    #================================get与set==============================
    @property
    def frame_sendMail(self):
        return self.frame_SMF
    @property
    def frame_addMail(self):
        return self.frame_SMadd
    @property
    def frame_mailList(self):
        return self.frame_SMList
    
    @property
    def lineEdit_ip(self):
        return self.lineEdit_ipadd
    @property
    def lineEdit_mail(self):
        return self.lineEdit_mailadd
    @property
    def lineEdit_user(self):
        return self.lineEdit_host
    @property
    def lineEdit_passcode(self):
        return self.lineEdit_pass
    @property
    def lineEdit_keys(self):
        return self.lineEdit
    
    @property
    def spin_day(self):
        return self.spinBox_day
    @property
    def combo_type(self):
        return self.comboBox_type
    @property
    def radio_up(self):
        return self.radioButton_up
    @property
    def radio_key(self):
        return self.radioButton_keys
    
    @property
    def button_start(self):
        return self.startButton
    @property
    def button_addIP(self):
        return self.pushButton_ipadd
    @property
    def button_delIP(self):
        return self.pushButton_deleteIP
    @property
    def button_clearIP(self):
        return self.pushButton_clearIP
    @property
    def button_loadIP(self):
        return self.pushButton_ipLoad
    
    
    @property
    def button_addMail(self):
        return self.pushButton_mailadd
    @property
    def button_delMail(self):
        return self.pushButton_delteMail
    @property
    def button_clearMail(self):
        return self.pushButton_clearMail
    @property
    def button_sendMail(self):
        return self.pushButton_sendMail
    @property
    def button_saveMail(self):
        return self.pushButton_saveMail
    @property
    def button_loadMail(self):
        return self.pushButton_mailLoad
    
    @property
    def button_clearInfo(self):
        return self.pushButton_clearInfo
    @property
    def button_saveInfo(self):
        return self.pushButton_saveInfo
    
    @property
    def list_ip(self):
        return self.listWidget_ip
    @property
    def list_mail(self):
        return self.listWidget_mail
    @property
    def list_info(self):
        return self.tableWidget
    
    #@property
    #def label_infoTip(self):
    #    return self.label_info
    @property
    def showHead(self):
        return self.SHOWHEAD
    @property
    def thread_start(self):
        return self.tStart
    @property
    def thread_send(self):
        return self.tSend
    
    #=================================控件的基础设置==========================
    def initGui(self):
        '''
            初始化窗口
        '''
        # 生成窗口
        self.setupUi(self)
        #设置窗口标题
        self.setWindowTitle(self.title)
        # 固定大小
        self.setMinimumSize(1023, 542)
        self.setMaximumSize(1023,542)
        # 隐藏一些Frame
        self.setCtlVisible()
        # 限制输入框
        self.setEdit()
        self.bindBtn()
        #self.list_ip.setVerticalScrollBarPolicy(2)
        self.show()
        
    def setCtlVisible(self):
        '''
            对Frame进行显示/隐藏
        '''
        # 设置
        self.frame_sendMail.setVisible(False)
        
        self.frame_addMail.setVisible(False)
        self.frame_mailList.setVisible(False)
    
    def setScrollBar(self):
        '''
            为控件添加滑动条
        '''
        # ip代理列表
        self.list_ip.setVerticalScrollBarPolicy(0)
        # 邮箱列表
        self.list_mail.setVerticalScrollBarPolicy(0)
        self.list_mail.setHorizontalScrollBarPolicy(0)
    def setEdit(self):
        '''
            对输入框进行限制， spin框，下拉框进行操作初始化, table表格初始化
        '''
        # 设置添加IP的输入框
        self.lineEdit_ip.setInputMask('000.000.000.000:00000;_')
        # 设置添加邮箱的输入框
        # 加入校验器
        regValidator = QtGui.QRegExpValidator(self)
        reg = QtCore.QRegExp('[a-zA-Z0-9._@\-]+$')
        regValidator.setRegExp(reg)
        # 限制 添加邮箱的输入框
        self.lineEdit_mail.setValidator(regValidator)
        # 限制 邮箱账号输入框
        self.lineEdit_user.setValidator(regValidator)
        # 设置 密码输入框
        self.lineEdit_passcode.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        
        # 设置天数计数器 天数限制：1-1000天
        self.spin_day.setRange(1, 1000)
        # 设置下拉框
        self.combo_type.addItems(self.spider.genres)
        
        # table表格初始化
        self.list_info.setColumnCount(len(self.showHead))
        self.list_info.setHorizontalHeaderLabels(self.showHead)
        # 禁止编辑
        self.list_info.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        # 关键字输入框
        self.lineEdit_keys.setPlaceholderText("分割符:,，、|和空格")
        
    def bindBtn(self):
        '''
            按钮事件绑定
        '''
        # 添加IP的按钮
        self.button_addIP.clicked.connect(self.clickedBtn_IPAdd)
        # 删除IP的按钮
        self.button_delIP.clicked.connect(self.clickedBtn_IPDel)
        # 清空IP的按钮
        self.button_clearIP.clicked.connect(self.clickedBtn_IPClear)
        # 导入IP的按钮
        self.button_loadIP.clicked.connect(self.clickedBtn_IPLoad)
        
        # 添加Mail的按钮
        self.button_addMail.clicked.connect(self.clickedBtn_MailAdd)
        # 删除Mail的按钮
        self.button_delMail.clicked.connect(self.clickedBtn_MailDel)
        # 清空Mail的按钮
        self.button_clearMail.clicked.connect(self.clickedBtn_MailClear)
        # 发送Mail的按钮
        self.button_sendMail.clicked.connect(self.clickedBtn_MailSend)
        # 保存Mail的按钮
        self.button_saveMail.clicked.connect(self.clickedBtn_MailSave)
        # 导入Mail的按钮
        self.button_loadMail.clicked.connect(self.clickedBtn_MailLoad)
        
        # 清空信息
        self.button_clearInfo.clicked.connect(self.clickedBtn_InfoClear)
        # 保存信息按钮
        self.button_saveInfo.clicked.connect(self.clickedBtn_InfoSave)
        # 监控按钮start
        self.button_start.clicked.connect(self.clickedBtn_Start)
    #================================按钮绑定函数============================
    def clickedBtn_IPAdd(self):
        '''
            添加IP
        '''
        # 获取输入框中合法的IP
        ip = self.checkIP(self.lineEdit_ip.text())
        if not ip:
            print("输入不合法")
            return
        self.list_ip.addItem(ip)
        # 把输入框中数据清空
        self.lineEdit_ip.clear()
    def clickedBtn_IPDel(self, item):
        '''
            删除指定IP
        '''
        self.list_ip.takeItem(self.list_ip.currentIndex().row())
    def clickedBtn_IPClear(self):
        '''
            清空列表IP
        '''
        if self.isSure('清空', '是否清空代理IP列表'):   
            self.list_ip.clear()
        else:
            return
    def clickedBtn_IPLoad(self):
        '''
            导入txt文件,将信息插入列表中
        '''
        filePath = self.findFile()
        try:
            for file in filePath:
                dataSet = FileSave.getTxt(file) # 返回一个生成器
                for line in dataSet:
                    # 判断iP是否合法
                    if self.checkIP(line):
                        self.list_ip.addItem(line)   # 将信息加入列表中
            
            return True
        except:
            self.infoTip(content='导入失败')
            return False
    #------------------------Mail----------------------------------
    def clickedBtn_MailAdd(self):
        '''
            添加mail
        '''
        text = self.lineEdit_mail.text().strip()
        if text:
            self.list_mail.addItem(text)
    def clickedBtn_MailDel(self):
        '''
            删除指定mail
        '''
        self.list_mail.takeItem(self.list_mail.currentIndex().row())
    def clickedBtn_MailClear(self):
        '''
            清空列表Mail
        '''
        # 是否确定清空
        if self.isSure('清空', '是否清空邮箱列表'):
            # 确定清空
            self.list_mail.clear()
        else:
            return
    def clickedBtn_MailSend(self):
        '''
            发送邮件
        '''
        self.statusBar.showMessage('正在发送邮箱')
        self.button_sendMail.setEnabled(False)
        # 是否发送
        filePath = self.findFile(filters='*', isMore=False)[0]
        # 如果中途退出，则不继续执行
        if not filePath:
            return
        
        self.thread_send.target = self.sendMail
        self.thread_send.obj = self.button_sendMail
        self.thread_send.args = (filePath, self.lineEdit_host.text().strip(), self.lineEdit_passcode.text(), self.list_mail)
        self.thread_send.start()
        #threading.Thread(target=self.sendMail, args=(filePath,)).start()
        
    def clickedBtn_MailSave(self):
        '''
            保存列表中的信息Mail
        '''
        dataSet = self.getListData(self.list_mail)
        self.saveFile(dataSet=dataSet)
    def clickedBtn_MailLoad(self):
        '''
            导入txt文件,将信息插入列表中Mail
        '''
        filePath = self.findFile()
        try:
            for file in filePath:
                dataSet = FileSave.getTxt(file) # 返回一个生成器
                for line in dataSet:
                    self.list_mail.addItem(line)   # 将信息加入列表中
            return True
        except:
            self.infoTip(content='导入失败')
            return False
    def clickedBtn_InfoClear(self):
        '''
            清除表单数据
        '''
        if self.isSure(content='是否确定清空数据'):
            self.list_info.setRowCount(0)
    def clickedBtn_InfoSave(self):
        '''
            保存爬取的数据
        '''
        self.saveFile(filters='*.csv', saveType='table', dataSet=self.spider.appList)
        
    def clickedBtn_Start(self):
        '''
            开启监控
        '''
        self.statusBar.showMessage('监控中')
        IpNums = self.list_ip.count()                           # 获取代理IP数量
        ipPoor = []
        
        if IpNums == 0:
            # 无代理IP则爬虫不启动代理IP功能
            self.spider.isProxy = False
        else:
            self.spider.isProxy = True
            for i in range(IpNums):
                ipPoor.append(self.list_ip.item(i).text())
            self.spider.proxyPoor = ipPoor
            
        self.button_start.setEnabled(False)                     # 让开始按钮无法继续按
        
        self.spider.day = self.spin_day.value()                 # 获取监控天数
        self.spider.jktype = self.radio_up.isChecked()          # 获取监控上/下架类型
        self.spider.apptype = self.combo_type.currentText()     # 获取监控的软件类别
        self.spider.search = self.getKeys()                     # 获取关键字:生成器或者None
        
        # 关键字处理成列表形式
        # 开启线程
        self.thread_start.target = self.startSpider
        self.thread_start.obj = self.button_start
        
        
        self.thread_start.start()
    
    #==================================================线程相关函数======================================

    def startSpider(self):
        '''
            启动爬虫
        '''
        status = self.spider.run()
        return status
    
    
    def sendStatus(self, status):
        '''
            邮箱发送结构反馈
        '''
        if status:
            # 发送成功
            self.infoTip(content='发送成功')
        else:
            self.infoTip(content='发送失败')
    
    def startStatus(self,status):
        '''
            监控结果反馈
        '''
        if status == 0:
            self.showInfo(self.spider.appList)
            self.statusBar.showMessage("监控成功!", 5000)
        elif status == -1:
            self.statusBar.showMessage("代理IP全部失效!", 5000)
            self.infoTip(content='代理IP全部失效!')
        else:
            self.statusBar.showMessage("出现未知错误!", 5000)
            self.infoTip(content='出现未知错误!!!')
    
    def sendMail(self,filePath, sender, passcode, list_mail):
        '''
            发送邮件
            参数：filePath文件路劲     
                sender:邮箱号
                passcode:授权码
                length:邮箱列表
        '''
        length = list_mail.count()
        receivers = []
            # 将邮箱列表的数据提取出来
        for i in range(length):
            receivers.append(list_mail.item(i).text())
        mail = MailSend.Mail(sender=sender, passcode=passcode, receivers=receivers)
        status = mail.sendFile(filePath = filePath)
        return status

    #================================其他函数===============================
    def checkIP(self, IP):
        '''
            检验输入的IP:Port是否合法
            None: 不合法
        '''
        try:
            pattenIP = '(1?\d{0,2}|2[0-4]\d|25[0-5]\.){3}(1?\d{0,2}|2[0-4]\d|25[0-5])'
            reg = re.compile(pattenIP)
            ip, port = IP.strip().split(':')
            port = int(port)
            # 如果合法
            #print(IP)
            if re.match(reg, ip) and 0<=port<=65535:
                return IP
            else:
                return None
        except:
            return None
    
    def isSure(self, title='注意', content='是否继续'):
        '''
            弹出一个消息框，询问是否确定该操作
            True:是的
            False:不继续
        '''
        yes = QtWidgets.QMessageBox.Yes
        no = QtWidgets.QMessageBox.No
        # 弹出对话窗
        replay = QtWidgets.QMessageBox.information(self, title, content, yes|no, no)
        if replay == yes:
            return True
        else:
            return False
    def infoTip(self, title='提示', content=''):
        '''
            弹出一个信息提示，但按钮OK
        '''
        ok =  QtWidgets.QMessageBox.Ok
        QtWidgets.QMessageBox.information(self, title, content, ok, ok)
        
    def getListData(self, listt):
        '''
            获取列表中所有信息
            返回值：生成器
        '''
        count = listt.count()
        for i in range(count):
            yield listt.item(i).text().strip()
    
    def findFile(self, filters='*.txt',isMore=True):
        '''
            打开文件对话框， 打开文件
            参数：允许显示的文件类型, isMore:True:多文件选择，否则单文件选择
            返回值：选择的文件地址 ：List类型
        '''
        # 判断是否为多选还是单选,因为单选返回的是一个string类型，故而要处理
        func = QtWidgets.QFileDialog.getOpenFileNames
        filePath = []
        opt = filePath.extend
        if not isMore:
            func = QtWidgets.QFileDialog.getOpenFileName
            opt = filePath.append
        
        fileNames, _ = func(self, '打开文件','.', filters)
        opt(fileNames)
        return filePath
                
    def saveFile(self, filters='*.txt', saveType='list', dataSet=[]):
        '''
            打开文件对话框，保存文件
            参数：filters:默认的保存后缀名
                saveType:保存的数据类型：list:将列表数据保存, table：将表格数据保存
                dataSet:数据
            #返回值：True:保存成功，否则失败
        '''
        
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, '保存文件', '.', filters)
        if saveType == 'list':
            # 保存列表数据
            func = FileSave.saveListToTxt
        else:
            # 保存表单数据
            func = FileSave.saveAppToCsv
        
        if func(filePath, dataSet):
            self.infoTip(content='保存成功')
            return True
        else:
            self.infoTip(content='保存失败')
            return False

            
    def getKeys(self, patten=r'[,，、| ]+'):
        '''
            获取关键字
            参数:patten为正则切割字符串的表达式
            返回值：关键字生成器
        '''
        keyStr = self.lineEdit_keys.text().strip()
        if not self.radio_key.isChecked() or not keyStr:
            # 如果没有设置关键字
            return None
        else:
            #print('----------',keyStr)
            keys = re.split(patten, keyStr)
            return keys
            #for key in keys:
                #yield key
    
    def showInfo(self, dataSet):
        '''
            将dataSet里的数据显示到list_info列表中
            参数dataSet：[{}，{}。。。]格式信息
            表中应显示：APP名称，发行商，应用类别，发行日期，下架日期
        '''
        row = len(dataSet)
        # 设置表行数
        self.list_info.setRowCount(row)
        # 获取表格列数
        column = self.list_info.columnCount()
        # 开始向表格插入数据
        for i in range(row):
            line = dataSet[i]
            for c in range(column):
                self.list_info.setItem(i, c, QtWidgets.QTableWidgetItem(line[self.showHead[c]]))