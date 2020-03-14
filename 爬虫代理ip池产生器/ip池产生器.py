import urllib
import re
import requests
import threading

HEADER = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
IPSET = []
# 网页下载器
def open_url(url):
    req = requests.get(url=url, headers=HEADER)
    return req.text

# 网页解析器
def findInfo(html):
    
    # 正则表达式设计
    ip = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>'
    port = r'<td>(\d*?)</td>'
    end = r'</tr>'
    infor = ip+'.*?'+port+'.*?'+end
    
    # 匹配信息
    reg = re.compile(infor, re.S)
    contents = re.findall(reg, html)

    # 合并ip与端口
    ipSet = []
    for ip, port in contents:
        ip = ip+':'+port
        ipSet.append(ip.strip())
    #print(ipSet)
    return ipSet


# 检测IP是否可行
def check_ip(proxy_url='', tmp=''):
    #post_url = 'http://icanhazip.com'
    post_url = 'https://httpbin.org/ip'
    proxies = {
        'http': 'http://{proxy_url}'.format(proxy_url=proxy_url),
        'https': 'https://{proxy_url}'.format(proxy_url=proxy_url),
    }
    
    proxy_ip = proxy_url.split(':')[0]
    try:
        feeback = requests.get(url=post_url, proxies=proxies, headers=HEADER, timeout=5)
        if proxy_ip in feeback.text:
            print('可用', proxy_url)
            #return True
            IPSET.append(proxy_url)
        else:
            print('不可用', proxy_url)
            #return False
    except:
        print('不可用2', proxy_url)
        #return False


# 存储器
def saveToTxt(filename, ipSet):
    with open(filename, 'w') as f:
        for ip in ipSet:
            f.write(ip+'\n')

if __name__ == '__main__':
    html = open_url('http://www.xicidaili.com/')
    IPSet = findInfo(html)
    '''
    for ip in IPSet:
        check_ip(ip)
    '''
    
    for ip in IPSet:
        threadd = threading.Thread(target=check_ip, args=(ip, ''))
        threadd.start()

    threadd.join()
    
    saveToTxt("代理IP池.txt", IPSET)
    #saveToTxt("代理IP池2.txt", IPSet)
    #saveToTxt("信息.txt", [html])
