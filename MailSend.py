import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
class Mail:
    def __init__(self, host='smtp.qq.com', sender='', passcode='', receivers=[]):
        self._host = host               # 设置服务器
        self._sender = sender           # 发件方
        self._passcode = passcode       # 授权码
        self._receivers = receivers     # 接受者池
    #===================================get与set==================================
    @property
    def host(self):
        return self._host
    @host.setter
    def host(self, val):
        self._host = val
    @property
    def sender(self):
        return self._sender
    @sender.setter
    def sender(self, val):
        self._sender = val
    @property
    def passcode(self):
        return self._passcode
    @passcode.setter
    def passcode(self, val):
        self._passcode = val
    @property
    def receivers(self):
        return self._receivers
    @receivers.setter
    def receivers(self, val):
        self._receivers = val
    
    #=================================发送功能=====================================
    def setMessage(self, title='禅大师软件监控信息', content = ''):
        '''
            功能：发送文本内容
        '''
        message = MIMEText(content, 'plain', 'utf-8')       # 设置内容，返回一个信息实列
        message['From'] = Header(self.sender, 'utf-8')      # 设置发件人姓名
        message['To'] = Header("you", 'utf-8')              # 设置收件人姓名
        message['Subject'] = Header(title, 'utf-8')         # 设置邮件标题
        
        return message
        
    def setFile(self, title='禅大师软件监控信息', filePath='', content=''):
        '''
            功能：发送带附件邮件
        '''
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header(self.sender, 'utf-8')
        message['To'] = Header("you", 'utf-8')
        message['Subject'] = Header(title, 'utf-8')
        message.attach(MIMEText(content, 'plain', 'utf-8'))     # 设置内容
        # 构造附件
        with open(filePath, 'rb') as f:
            att = MIMEText(f.read(), 'plain', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = 'attachment;filename = "info.csv"'
            message.attach(att)
        #att1 = MIMEText(open(filePath, 'rb').read(), 'base64', 'utf-8')
        #att1['Content-Type'] = 'application/octet-stream'
        #att1["Content-Disposition"] = 'attachment; filename="软件监控信息.csv"'
        #message.attach(att1)
        return message
    
    def send(self, message):
        try:
            smtpObj = smtplib.SMTP()                        # 创建smtp实列
            smtpObj.connect(self.host, 25)                  # 连接上邮箱服务器
            smtpObj.login(self.sender, self.passcode)       # 登陆自己的邮箱smtp
            smtpObj.sendmail(self.sender, self.receivers, message.as_string()) # 发送邮件
            #print("邮件发送成功")
            return True
        except:
            #print("发送失败")
            return False
    
    def sendFile(self, title='禅大师软件监控信息', filePath='', content=''):
        message = self.setFile(filePath=filePath, content=content)
        if self.send(message):
            return True
        else:
            return False
if __name__ == '__main__':
    receivers = ['2074748362@qq.com']
    #mail = Mail(sender='', passcode='', receivers=receivers)
    #message = mail.setMessage(content='就是这样子')
    message = mail.setFile(filePath = 'C:/Users/HEART/Desktop/禅大师上下架软件监控/test.csv', content='nihao')
    mail.send(message)
