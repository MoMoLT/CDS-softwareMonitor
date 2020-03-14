import requests  # 需要pip安装
import json
#import re
#import urllib
import threading 
import DateTime
import time
#import csv
'''
https://www.chandashi.com/bang/delistdata/genre/0/date/2020-03-11.html?page=1&order=rank
https://www.chandashi.com/bang/delistdata/genre/0/date/2020-03-11/search/%E6%A3%8B%E7%89%8C.html?page=0&order=rank
禅大师爬虫
外部输入：监控天数，监控类型与类别，关键字集合，代理ip集合
'''
class CDSSpider:
    # 外部输入：监控的天数，监控类型
    def __init__(self, day=1, isUp=True, apptype='所有', search=None, proxyPoor=None):
        self._header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'
                }
        self._proxyPoor = proxyPoor                     # 代理池
        self.ip = ''                                # 当前的代理IP
        self.maxThread = 70                         # 最大线程数量
        #-----------------------------------------外部接口参数--------------------------------------------------
        
        self._day = day                             # 监控天数
        #self._jktype = jktype                      # 监控上/下类型
        self._jktype = isUp
        self._apptype = apptype                     # 监控app类别
        self._search = search                       # 监控关键字
        
        self._appList = []
        
        # 监控上/下架类型，信息存放在网站的哪个文件中，这个是网站定的
        self._GENRES = {
            '所有':'0',
            '所有应用':'5000',
            '所有游戏':'6014',
            '商务应用':'6000',
            '天气应用':'6001',
            '工具应用':'6002',
            '社交应用':'6005',
            '桌面游戏':'7004',
            '卡牌游戏':'7005',
            '音乐游戏':'7011',
        }
        #---------------------------------------------url设置---------------------------------------------------
        self.base_url = 'https://www.chandashi.com'             # 基网址
        self.down_url_head = '/bang/delistdata/genre/'          # 应用下架url前段固定部分
        self.up_url_head = '/bang/weekdata/genre/'              # 应用上架url前段固定部分
        self.nosearch_url = '{apptypeID}/date/{date}.html?page={page}&order=rank' # 无关键词搜索，返回xml信息
        self.search_url = '{apptypeID}/date/{date}/search/{search}.html?page={page}&order=rank' # 有关键词搜索，一次只能搜索一个
        self.app_url = self.base_url + '/apps/view/appId/{appId}/country/cn.html'   # app信息url
        
        #---------------------------------------------正则表达式设置---------------------------------------------
        self.re_down_url = r'<li><a href="(.*?)">App Store 下架监控</a></li>'            # 下架监控url的正则表达式
        self.re_up_url = r'<li><a href="(.*?)">App Store 新品发现</a></li>'              # 上架url的正则表达式
        self.re_down_num = r'px;">(.*?)</span>个下架'                                   # 下架个数的正则表达式
        self.re_up_num = r'px;">(.*?)</span>个新品'                                     # 上架个数的正则表达式
        
        #---------------------------------------------GUI控件控制设置--------------------------------------------
        self.START = False                                      # 启动爬虫状态
        self.ISPROXY = False                                    # 启动代理
        self.OKPROXY = True                                     # 代理IP池里的IP是否有用
        #self.PAUSE = False                                      # 暂停爬虫状态
    #============================================get与set================================================
    # 浏览器的user-agent信息
    @property
    def header(self):
        return self._header
    # 代理ip池，接受的是一个生成器
    @property
    def proxyPoor(self):
        return self._proxyPoor
    @proxyPoor.setter
    def proxyPoor(self, val):
        self._proxyPoor = val
    # 监控天数
    @property
    def day(self):
        return self._day
    @day.setter
    def day(self, val):
        self._day = int(val)
    # 监控上/下架类型
    @property
    def jktype(self):
        return self._jktype
    @jktype.setter
    def jktype(self, val):
        self._jktype = val
    # 监控类别
    @property
    def apptype(self):
        return self._GENRES[self._apptype]
    @apptype.setter
    def apptype(self, val):
        self._apptype = val
    # 监控的关键字集合, 生成器
    @property
    def search(self):
        return self._search
    @search.setter
    def search(self, val):
        self._search = val
    # 内部读取数据集
    @property
    def appList(self):
        return self._appList
    @appList.setter
    def appList(self, val):
        self._appList = val
    # 外部读取
    '''
    @property
    def dataSet(self):
        for app in self.appList:
            yield app
    '''
    # 类别 返回列表,关键字列表
    @property
    def genres(self):
        return list(self._GENRES.keys())
    
    # 爬虫状态
    @property
    def isStart(self):
        return self.START
    @isStart.setter
    def isStart(self, val):
        self.START = val
    # 启动代理？
    @property
    def isProxy(self):
        return self.ISPROXY
    @isProxy.setter
    def isProxy(self, val):
        self.ISPROXY = val
    @property
    def okProxy(self):
        return self.OKPROXY
    @okProxy.setter
    def okProxy(self, val):
        self.OKPROXY = val
    @property
    def IP(self):
        return self.ip
    @IP.setter
    def IP(self, val):
        self.ip = val
    #==========================================IP检测工具================================================
    '''
    def checkIP(self, ip):

            #检测IP是否可用，用它来测试一个网站是否返回数据
        
        post_url = 'http://icanhazip.com'#self.base_url

        proxies = {
            'http': 'http://{proxy_url}'.format(proxy_url=ip),
            'https': 'https://{proxy_url}'.format(proxy_url=ip),
        }
        proxy_ip = ip.split(':')[0]
        try:
            feeback = requests.get(url=post_url, proxies=proxies, headers=self.header, timeout=5)
            print(feeback)
            if proxy_ip in feeback:
                return True
            
        except:
            return False
    '''
    def getIP(self):
        '''
        for ip in self.proxyPoor:
            if self.checkIP(ip):
                return ip
        # 否则，无代理IP可用了
        self.okProxy = False
        return None
        '''
        print(self.proxyPoor)
        try:
            ip = self.proxyPoor.pop()
            return ip
        except:
            return None
    #=========================================下载器=====================================================
    # 下载服务器反馈的信息
    def open_url(self, url):
        res = None
        print(url)
        if not self.isProxy:
            #print("最后没有代理了")
            # 不启用代理
            res = requests.get(url, headers=self.header)
        else:
            # 启动代理
            count = 0
            self.IP = self.getIP()
            print(self.okProxy, self.IP)
            while self.okProxy and self.IP and count<20:
                print("换了一个IP", self.IP)
                # 如果IPPorr池里的代理IP都失效了，就退出
                try:
                    proxies = {
                        'http': 'http://{proxy_url}'.format(proxy_url=self.IP),
                        'https': 'https://{proxy_url}'.format(proxy_url=self.IP),
                    }
                    res = requests.get(url, headers=self.header, proxies=proxies, timeout=4)
                    #print(res)
                    return res
                except:
                    # Ip失效
                    self.IP = self.getIP()      # 重新获取一个可用IP
                    count += 1
                    
        return res
    # 下载xml信息, 返回json格式信息
    def down_xml(self, url):
        res = self.open_url(url)
        j = json.loads(res.text)
        return j
    #=======================================分析器========================================
    '''
    主要信息：
    app名字trackName
    发行商sellerName，
    发布时间releaseDate
    下架时间offlineDate
    价格price, 类别genre
    Apple ID: trackId
    链接：获取trackId拼接
    '''
    def get_A_Info(self, data):
        '''
            提取一条信息中的关键信息，加入到self.appList中
        '''
        if self.jktype:
            # 如果为上架监控， 没有下架时间
            data['offlineDate'] = ''
        link = self.app_url.format(appId=data['trackId'])
        self.appList.append({
                'APP':data['trackName'],
                '发行商':data['sellerName'],
                '发布时间':data['releaseDate'],
                '下架时间':data['offlineDate'],
                '价格':data['price'],
                '类别':data['genre'],
                'ID':data['trackId'],
                '链接':link,
                })
        
    def get_xml_Info(self, xml):
        '''
            提取一份xml信息关键信息：使用线程
        '''
        dataSet = xml['data']
        #print(len(dataSet))
        # 如果无数据，则返回False
        if not dataSet:
            return False
        
        threads = []
        # 创建线程
        for data in dataSet:
            t = threading.Thread(target=self.get_A_Info, args=(data,))
            threads.append(t)
        # 启动线程
        for t in threads:
            t.start()
            while True:
                if len(threading.enumerate()) <= self.maxThread:
                    break
                
        return True
    
    def get_noserach_day_Info(self, date):
        '''
            提取一天内的xml信息, 参数day格式2020-3-11， 无关键词搜索
        '''
        # 获取一个无关键字搜素url
        url = self.getUrl()
        # page=0即爬取所有的信息
        url = url.format(apptypeID=self.apptype, date=date, page=0)
        xml = self.down_xml(url)
        if not self.get_xml_Info(xml):
            print("空的")
            return False
        return True
    
    def get_search_day_Info(self, date, search):
        '''
            有关键字搜索，一次搜一个关键字
        '''
        url = self.getUrl(True)
        url = url.format(apptypeID=self.apptype, date=date, search=search, page=0)
        xml = self.down_xml(url)
        if not self.get_xml_Info(xml):
            print("空的")
            return False
        return True
    
    
            
    #=====================================其他函数方法=====================================
    def getUrl(self, tyS=False):
        '''
            获取一个待格式化的url, tyS：False即无关键字，True有关键字
        '''
        url = self.base_url
        if self.jktype:
            # 为上架监控时
            url += self.up_url_head
        else:
            url += self.down_url_head
            
        if tyS:
            # 含有关键字时
            url += self.search_url
        else:
            url += self.nosearch_url
        return url
    
    def run(self):
        '''
            爬虫启动函数
            返回值：0：成功，-1IP代理全部失效，1未知失败
        '''
        try:
            self.okProxy = True
            self.appList = []
            self.isStart = True
            # 从当前天数开始,往前推算
            if self.search:
                print(self.search)
                for day in range(self.day):
                    # 将倒数天数转为2020-03-11格式
                    date = DateTime.getDate(day+1)
                    
                    for key in self.search:
                        # 从关键字集合中取出每一个关键字,进行爬取
                        self.get_search_day_Info(date, key)
                        # 进行爬取时，延时3秒
                        time.sleep(3)
            else:
                #无关键字爬取
                for day in range(self.day):
                    #print(day)
                    date = DateTime.getDate(day+1)
                    self.get_noserach_day_Info(date)
                    time.sleep(3)
                    
            self.isStart = False
            return 0
        except:
            if not self.okProxy:
                # 如果代理池的IP全失效了
                print("失效的IP")
                return -1
            print("未知错误")
            return 1

if __name__ == '__main__':
    spider = CDSSpider(day=1)
    spider.run()
    print(spider.appList)