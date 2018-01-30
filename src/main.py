#/usr/bin/env python3
# -*- coding:UTF-8 -*-

import requests
import os

base_url = 'http://huaban.com/boards/favorite/beauty/'
params = {
    'j0ga0hbi': '',
    'max': '1062161596',
    'limit': '100',
    'wfl': '1'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}

# 花瓣图片cdn域名
img_domain = 'http://img.hb.aicdn.com/'

# 文件后缀
file_suffix = {
    'image/jpeg':'.jpg',
    'image/png':'.png'
}
local_image_dir = 'images'


# 下载文件
def download(downloadUrl, fileName):
    file_path = local_image_dir + os.path.sep + fileName
    remote = requests.get(downloadUrl)
    with open(file_path, 'wb') as fo:
        fo.write(remote.content)

# 解析主页面
def get_main_url():

    try:
        response = requests.get(url=base_url, params=params, headers=headers)
        if response.status_code != 200:
            print('地址访问失败，状态码为', response.status_code)
            return

        # print('打印整个页面的返回值>>>', response.text)

        boards = response.json()['boards']
        i = 0
        for board in boards:
            for pin in board['pins']:
                i += 1
                download_url = img_domain + pin['file']['key']
                filename = (str(pin['file_id']) + file_suffix[pin['file']['type']])
                print('下载第', str(i), '张图，地址：', download_url, '保存到本地到文件名', filename)
                download(download_url, filename)

    except Exception as e:
        print(e)

if __name__ == "__main__":

    if not os.path.exists(local_image_dir):
        # 创建目录
        os.makedirs(local_image_dir)

    get_main_url()

