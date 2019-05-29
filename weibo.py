import requests
import urllib
import time
import os
import time_standard as tst
from tqdm import tqdm
from urllib.parse import urlencode
from pyquery import PyQuery as pq

# 基础数据
host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0'

user_id = str(input("请输入待抓取微博用户ID："))  #str(5222241375)
headers = {
    'Host': host,
    'Refer': 'https://m.weibo.cn/u/%s' % user_id,
    'User-Agent': user_agent
}


def get_single_page(page):
    """
    构造url的get参数并访问
    page：页数
    return：json对象
    """
    params = {
        'type': 'uid',
        'value': int(user_id),
        'containerid': int('107603'+user_id),
        'page': page
    }
    url = base_url+urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)


def analysis_page(json, pic_filebagPath):
    items = json.get('data').get('cards')
    for item in items:
        item = item.get('mblog')
        if item:
            data = {
                'created_at': item.get('created_at'),
                'text': pq(item.get('text')).text(),
                'attitudes': item.get('attitudes_count'),
                'comments': item.get('comments_count'),
                'reports': item.get('reposts_count')
            }
            base_data[len(base_data)] = data
            pics = item.get('pics')
            if pics:
                for pic in pics:
                    picture_url = pic.get('large').get('url')
                    pic_name = tst.timestr_standard(data['created_at'])
                    download_pics(picture_url, pic_name, pic_filebagPath)


def download_pics(pic_url, pic_name, pic_filebagPath):
    pic_filePath = pic_filebagPath+'\\'
    try:
        if pic_url.endswith('.jpg'):
            f = open(pic_filePath+str(pic_name)+'.jpg', 'wb')
        if pic_url.endswith('.gif'):
            f = open(pic_filePath+str(pic_name)+'.gif', 'wb')
        f.write(requests.get(pic_url).content)
        f.close()
    except Exception as e:
        print(pic_name+'error', e)
    time.sleep(0.1)


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("创建目录", path)


currentRoot = os.getcwd()
t = time.strftime('%Y-%m-%d', time.localtime())
root = currentRoot+"\\photoWeibo"+t+"\\"

#if __name__ == '__main__':
base_data = {}
page = 0  # 页数
time_start = time.time()
try:
    json = get_single_page(1)
    # 微博主名称
    screen_name = json.get('data').get('cards')[0].get(
        'mblog').get('user').get('screen_name')
    # 发送微博总条数(包括转发,转发的微博无法获取图片)
    total = json.get('data').get('cardlistInfo').get('total')
    # 图片下载路径建立
    pic_filebagPath = root+screen_name
    if os.path.exists(pic_filebagPath) == False:
        os.makedirs(pic_filebagPath)
        print("创建目录", pic_filebagPath, ",用来存储图片")

    page = total//10 if total % 10 == 0 else total//10+1
    print('总页数为：%s' % page)

    for page in tqdm(range(0, page)):
        json = get_single_page(page)
        analysis_page(json, pic_filebagPath)
except Exception as e:
    print('error:', e)
finally:
    time_end = time.time()
    print('\n totally cost', time_end-time_start)  # 显示程序运行时间

input("输入任意值结束程序：")