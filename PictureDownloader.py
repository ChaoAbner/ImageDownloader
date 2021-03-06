# encoding = 'UTF-8'
__author__ = '_chao'


import requests,urllib
import re
import sys
import socket
import os

from urllib import request


headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.9 Safari/537.36',
    'cookie':'BAIDUID=DA4019EA9B9C2455A0D0518917126251:FG=1; BIDUPSID=DA4019EA9B9C2455A0D0518917126251; PSTM=1519563931; BDUSS=5BVjZGeVczVGlWb2plc2NrVVNhOFRGczdaaUQ3aHZ5dURlZDZVYXF4UkFPc3BhQVFBQUFBJCQAAAAAAAAAAAEAAADdyqxfWWNXZWlkb2xpZWIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAECtolpAraJaYm; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1441_21088; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=ala; BDRCVFR[tox4WRQ4-Km]=mk3SLVN4HKm'
}


old_url = []                                                                # 用来存放已经下载过的url

def download_imgs(html,word):
        socket.setdefaulttimeout(3)                                         # 对整个socket层设置超时时间
        tank_url = []                                                       # 存放匹配到的url
        img_urls = re.findall(r'"objURL":"(.*?)",',html)                    # 取"objURL":"和“，中间的那段
        tank_url.append(img_urls)                                           # 向tank_url中添加url
        for urls in tank_url:                                               # urls为一个列表中的多个url
            for url in urls:
                if url not in old_url:                                      # 判断是否为下载过的url，不是即下载
                    try:
                        pic = requests.get(url,timeout=5)                   # 设定请求超时5秒
                        if pic.status_code == 200:                          # 请求状态码为200（正常）的才下载
                            old_url.append(url)
                            print('正在下载第%s张的图片...' % (len(old_url))) # 获取old_url中的元素个数即可知道当前图片个数
                            request.urlretrieve(url, r'D:/'+filemane+'/img_%s.jpg' %len(old_url))
                            print('下载完成\n-------------')
                        else:
                            print('【网站请求错误！】---404')                  
                    except  Exception as e:
                        print('【网站异常！】：',e)
                else:
                    print('【已过滤重复图片】')


if __name__ == '__main__':
    print('='*20 + '欢迎使用超超图片下载软件' + '='*20 + '\n')
    print('*'*40 + '\n')
    
    path = r'D:'
    filemane = input('_________________请输入存放图片的文件夹名（默认在D盘，文件名不能重复！）： ')
    os.path.isdir(path)                                                                                         # 没有not时，创建文件夹。加not为存在文件夹时，继续存入。---if not...
    os.mkdir(os.path.join(path, filemane))                                                                      # 在该路径创建一个文件夹
    print('                 【创建成功！】\n')
    word = input('_________________请输入搜索关键字 : ' )
    word = word.encode('utf-8')                                                                                 # 将输入的中文字符串转化成utf-8格式(十六进制)，此时word = 'xe4\xb8\xad\xe6\x96\x87'
    s = urllib.request.quote(word.decode(sys.stdin.encoding).encode('utf8'))                                    # 再将十六进制中文转化为url编码格式，如s = '%2%3%q'
    for page in range(0,1181,20):                                                                               # 每隔20换一个页面      
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+s+'&pn={}&gsm='.format(page)    # 实现翻页，获取大量url
        response = requests.get(url,headers = headers)                                                          # 请求url
        if response.status_code == 200:                                                                         # 当状态吗为200时，才执行下载操作
            html = response.text                                                                                # 将获取的相应解析出来
            download_imgs(html, word)                                                                           # 给下载器函数传入解析页面信息和输入关键字
        else:
            pass
    exit(0)
