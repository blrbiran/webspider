# coding: utf8
import urllib.request
import chardet
import re
import numpy as np

basic_url = "http://gdjy.hfut.edu.cn"
show_index = 1

def subStringHtml(template):
    rule = r'<a href="/companys/[0-9]+\.html">.*</a>'
    slotList = re.findall(rule, template)
    return slotList

def getHrefData(hreflink):
    rule = r'<a href="(.*?)">(.*?)</a>'
    data = re.findall(rule, hreflink)
    return data

def searchContext(data, keywords):
    rekeys = ""
    for index, value in enumerate(keywords):
        if index == 0:
            rekeys += value
        else:
            rekeys += "|" + value
    # print(rekeys)
    rule = '^.*?(' + rekeys + ').*?$'
    # rule = '.*' + keywords[0] + '+.*'
    # print(rule)
    # rule = keywords(0)
    # data = re.findall(rule, data, flags=re.DOTALL+re.S)
    data = re.findall(rule, data, flags=re.M)
    keyappear = np.unique(data)
    # print(keyappear)
    if keywords[0] in keyappear:
        return True, keyappear
    else:
        return False, keyappear


def searchLink(urldata, keyword):
    global show_index
    name = urldata[1]
    url = basic_url + urldata[0]
    page = urllib.request.urlopen(url).read().decode('utf-8')
    valid, dataList = searchContext(page, keyword)
    if valid:
        print(str(show_index) + ". " + name)
        show_index += 1
        print(url)
        print(dataList)

def searchIndex(index, keyword):
    indexpage = urllib.request.urlopen(basic_url + '/companys/list.html?page=' + str(index)).read().decode('utf-8')

    # print(indexpage)
    # print(chardet.detect(indexpage))

    slotList = subStringHtml(indexpage)
    for slot in slotList:
        searchLink(getHrefData(slot)[0], keyword)

if __name__ == "__main__":
    keywords = ["法学", "经济", "计算机", "土木", "四川"]
    # searchIndex(1, keywords)
    for index in range(1,23):
        searchIndex(index, keywords)

    # searchLink(("/companys/434.html","123"), ["法学", "安徽"])
    # print("法".encode("utf-8"))
    # print(unicode('法','utf-8'))