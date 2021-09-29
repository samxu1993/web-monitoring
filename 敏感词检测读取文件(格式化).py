# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: 敏感词检测读取文件(格式化).py
# @Author: SamXss
# @Institution: --- University, ---, China
# @E-mail: SamXss0101@gmail.com
# @Site: 
# @Time: 9月 14, 2021
# ---
# -*- coding:utf-8 -*-

from datetime import datetime
from requests import get
from requests.packages import urllib3
from html.parser import HTMLParser
from urllib.parse import urlparse
from collections import Counter


urllib3.disable_warnings()


# AC自动机算法
class node(object):
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        self.word = ""


class ac_automation(object):

    def __init__(self):
        self.root = node()

    # 添加敏感词函数
    def addword(self, word):
        temp_root = self.root
        for char in word:
            if char not in temp_root.next:
                temp_root.next[char] = node()
            temp_root = temp_root.next[char]
        temp_root.isWord = True
        temp_root.word = word

    # 失败指针函数
    def make_fail(self):
        temp_que = []
        temp_que.append(self.root)
        while len(temp_que) != 0:
            temp = temp_que.pop(0)
            p = None
            for key, value in temp.next.item():
                if temp == self.root:
                    temp.next[key].fail = self.root
                else:
                    p = temp.fail
                    while p is not None:
                        if key in p.next:
                            temp.next[key].fail = p.fail
                            break
                        p = p.fail
                    if p is None:
                        temp.next[key].fail = self.root
                temp_que.append(temp.next[key])

    # 查找敏感词函数
    def search(self, content):
        p = self.root
        result = []
        currentposition = 0

        while currentposition < len(content):
            word = content[currentposition]
            while word in p.next == False and p != self.root:
                p = p.fail

            if word in p.next:
                p = p.next[word]
            else:
                p = self.root

            if p.isWord:
                result.append(p.word)
                p = self.root
            currentposition += 1
        return result

    # 加载敏感词库函数
    def parse(self, path):
        # with open(path, encoding='gb2312') as f:
        with open(path) as f:

            for keyword in f:
                self.addword(str(keyword).strip())

    # 敏感词替换函数
    def words_replace(self, text):
        """
        :param ah: AC自动机
        :param text: 文本
        :return: 过滤敏感词之后的文本
        """
        result = list(set(self.search(text)))
        for x in result:
            m = text.replace(x, '*' * len(x))
            text = m
        return text

    # 网页敏感词检测
    def page(self, url):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38"
            }
            response = get(url, headers=header, verify=False)
            response.encoding = "utf-8"
            word = ah.search(response.text)
            if len(word) == 0:
                pass
            else:
                dt_ms1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                word_count = Counter(word)
                word_list = ",".join(set(word_count.elements()))
                Sensitive = {"type": "敏感词", "取数时间": dt_ms, "web_url": web_url,
                       "敏感链接": url,
                       "敏感词": word_list, "最近监测时间": dt_ms1, "处置状态": "未处置"}
                print(Sensitive)
            return response.text
        except:
            pass
            return None


# HTML 解析器
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
                    if "http" in value:
                        # 暗链检查
                        my.parse_url(web_url, value)

                        # print('总共耗时：' + str(time4 - time1) + 's')
                    else:
                        values = web_url[:-1] + value + "/"
                        my.parse_url(web_url, values)
    def parse_url(self, url, value):
        # print(url,value)
        if urlparse(url).netloc.split(".", 1)[1] in value:
            # print(value, "是再相同域名下！")
            ah.page(value)
        else:
            # print(value, "疑似暗链继续检查网站")
            ah.page(value)


if __name__ == '__main__':
    dt_ms = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ah = ac_automation()
    my = MyParser()
    path = r'ciku_baokong.txt'
    ah.parse(path)
    # ah.parse(argv[1])
    with open("url.txt",encoding="gb2312")as f:
        for web_url in f:
            web_url=web_url.split("\n")[0]
            print(web_url)
            my.feed(ah.page(web_url))
