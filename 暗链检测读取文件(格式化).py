# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: 暗链检测读取文件(格式化).py
# @Author: SamXss
# @Institution: --- University, ---, China
# @E-mail: SamXss@gmail.com
# @Site: 
# @Time: 9月 14, 2021
# ---

from re import findall
from datetime import datetime
from requests import get
from requests.packages import urllib3
from html.parser import HTMLParser
from urllib.parse import urlparse

urllib3.disable_warnings()


class ac_automation(object):


    # 获取初始网页全部信息
    def page(self, url):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
            }
            response = get(url, headers=header, verify=False)
            response.encoding = "utf-8"
            return response.text
        except:
            pass

    # 网页暗链检测
    def check_page(self, url):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
            }
            response = get(url, headers=header, verify=False, timeout=2)
            response.encoding = "utf-8"
            # print(response.text)
            # print(url)
            dt_ms1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            title = findall('<title>(.+)</title>', response.text)
            exception_msg=url+title[0]
            Dark_chain = {"type": "黑链/挂马", "取数时间": dt_ms, "web_url": web_url,
                           "异常url":url, "异常信息":exception_msg,
                          "事件类型": "恶意网站", "发现时间": dt_ms1, "更新时间": dt_ms1, "处置状态": "未处置"}
            print(Dark_chain)

            return response.text
        except:
            pass


# HTML 解析器获取A标签
class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        # 这里重新定义了处理开始标签的函数
        if tag == 'a':
            # 判断标签<a>的属性
            for name, value in attrs:
                if name == 'href':
                    # print(value,"zheshi ciyic ")
                    # 暗链检查
                    if "http" in value:
                        # 暗链检查
                        my.parse_url(web_url, value)
                    else:
                        values = web_url[:-1] + value + "/"
                        my.parse_url(web_url, values)

    def parse_url(self, url, value):
        if urlparse(url).netloc.split(".", 1)[1] in value:
            # print(value, "是再相同域名下！")
            # ah.page(value)
            ah.check_page(value)
            pass
        else:
            print(value, "疑似暗链继续检查网站")
            ah.check_page(value)


if __name__ == '__main__':
    dt_ms = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ah = ac_automation()
    my = MyParser()
    # web_url = "https://xn--ehq01tnu8a5dv.xyz/?fulione"
    with open("url.txt", encoding="gb2312")as f:
        for web_url in f:
            web_url = web_url.split("\n")[0]
            print(web_url)
            my.feed(ah.page(web_url))


