import threading
import requests

HEADER = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
# 检测IP是否可用
def check_ip(proxy_url='', test=''):
    post_url = 'https://httpbin.org/ip'

    proxies = {
        'http': 'http://{proxy_url}'.format(proxy_url=proxy_url),
        'https': 'https://{proxy_url}'.format(proxy_url=proxy_url),
    }
    header = {
        'Host': 'httpbin.org',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',

    }
    # print(proxies)
    proxy_ip = proxy_url.split(':')[0]
    try:
        feeback = requests.get(url=post_url, proxies=proxies, headers=HEADER, timeout=5)
        if proxy_ip in feeback.text:
            print("可用")
            return 1
        else:
            print("不可用")
            return 0
    except:
        print("不可用")
        return 0

if __name__ == '__main__':
    while True:
        ip = input().strip()
        print(ip)
        print(check_ip(ip))
