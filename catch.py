import re
import requests
import time
import os

url = "http://tieba.baidu.com/p/2460150866"
currentRoot = os.getcwd()
t = time.strftime('%Y-%m-%d', time.localtime())
root = currentRoot+"\\photoPY"+t+"\\"


# 图片url列表逐条下载
def Download1(imglist):
    x = 1
    for imgurl in imglist:
        imgres = requests.get(imgurl)
        with open(root+"{}.jpg".format(x), "wb") as f:
            f.write(imgres.content)
        x = x+1
        print("第", x, "张")


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("创建目录", path, ",用来存储图片")


response2 = requests.get(url)
imglist = re.findall('bpic="(.+?\.jpg)" class', response2.text)
mkdir(root)
Download1(imglist)
