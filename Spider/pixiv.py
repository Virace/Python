#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 22:15
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : pixiv.py
# @Software: PyCharm

# 还有待优化，cookie需要自己抓。
# 还需要挂代理
# 图片很大，代理如果很渣会很难受。感觉可以用aria2下载

import re
import requests

headers = {'Cookie': 'PHPSESSID=xxxxx'}

proxies = {
    "http": "127.0.0.1:10086",
    "https": "127.0.0.1:10086",
}


def get_list_for_id(_id):
    """
    先根据pixiv 用户ID 获取全部图片ID
    :param _id:
    :return:
    """
    url = 'https://www.pixiv.net/ajax/user/{}/profile/all'.format(_id)
    res = requests.get(url=url, headers=headers, proxies=proxies)
    source = res.json()
    if not source['error']:
        return [item for item in source['body']['illusts']]


def get_img_url(_id, img_id_list, url_list):
    """
    根据图片ID获取 图片地址
    :param _id: 用户ID
    :param img_id_list: 图片ID列表
    :param url_list: 图片地址列表
    :return:
    """
    # 每次请求获取最大100个图片
    ids = ['ids[]={}&'.format(item) for item in img_id_list[:100]]

    url = 'https://www.pixiv.net/ajax/user/{}/profile/illusts?{}is_manga_top=0'.format(_id, ''.join(ids))
    res = requests.get(url=url, headers=headers, proxies=proxies)
    source = res.json()['body']['works']
    tpl = "https://i.pximg.net/img-original/img/{}_p0.png"
    # 格式化URL 并且加入到img_id_list中
    url_list.extend([tpl.format(re.compile("/img/(.*)_p0_").findall(value['url'])[0]) for _, value in source.items()])
    # 如果ID列表大于100个则递归
    if len(img_id_list) > 100:
        get_img_url(_id, img_id_list[101:], url_list)


def download_img(url):

    try:
        res = requests.get(url=url, headers={'referer': 'https://www.pximg.net'}, proxies=proxies)
    except:
        print('下载错误', url)
    else:
        with open('./img/' + url.split('/')[-1], 'wb+') as file:
            for chunk in res.iter_content(10000):
                file.write(chunk)


def main(_id):
    ilist = get_list_for_id(_id)
    img_list = list()
    get_img_url(_id, ilist, img_list)
    print('共{}张图片' .format(len(img_list)))
    i = 1
    for item in img_list:
        print('当前下载第{}张'.format(i))
        download_img(item)
        i += 1
    print('全部下载完毕')


if __name__ == '__main__':
    main(27517)
