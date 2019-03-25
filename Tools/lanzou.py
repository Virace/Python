#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 19:48
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : lanzou.py
# @Software: PyCharm

import os
import requests
import mimetypes

from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder


def login(username, password):
    """
    根据用户名密码登录蓝奏云，登录成功则返回cookie,失败则返回错误信息
    :param username:
    :param password:
    :return:
    """
    url = 'https://up.woozooo.com/account.php'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'action': 'login',
        'task': 'login',
        'ref': '',
        # 这个值不清楚是否会变，如果会变就先取一下
        'formhash': '55174221',
        'username': username,
        'password': password
    }
    res = requests.post(url, data=data, headers=headers)

    soup = BeautifulSoup(res.text, 'lxml')
    # 查找错误信息
    info = soup.find('div', {'align': 'center'})
    if info:
        return 'error', info.get_text()
    else:
        return 'success', ';'.join(['{}={}'.format(key, value) for key, value in res.cookies.items()])


def upload(cookies, file):
    """
    上传文件，需要登录Cookie 和 文件路径
    :param cookies:
    :param file:
    :return: 上传成功返回文件地址，失败这返回错误信息
    """
    url = 'https://pc.woozooo.com/fileup.php'
    # 拼接
    multipart_encoder = MultipartEncoder(fields={
        'task': (None, '1'),
        # 上传文件夹ID
        'folder_id': (None, '-1'),
        'id': (None, 'WU_FILE_1'),
        # 文件名
        'name': (None, os.path.basename(file)),
        # 文件类型 mime-type
        'type': (None, mimetypes.guess_type(file)[0]),
        # 最后修改时间
        'lastModifiedDate': (None, str(os.path.getmtime(file))),
        # 文件大小
        'size': (None, str(os.path.getsize(file))),
        # 文件
        'upload_file': (os.path.basename(file), open(file, 'rb'))
    })
    res = requests.post(
        url,
        data=multipart_encoder,
        headers={'Content-Type': multipart_encoder.content_type,
                 'Cookie': cookies}
    )
    source = res.json()
    # 判断是否上传成功
    if source['zt'] == 1:
        return 'success', '{}/{}'.format(source['text'][0]['is_newd'], source['text'][0]['f_id'])
    else:
        return 'error', source['info']


class Lanzou(object):
    """
    用类操作，可能更符合当前要求，如果使用的话大家可以把代码都移过来，这只是个简单封装
    """
    def __init__(self, username, password):
        self.cookie = login(username, password)
        if self.cookie == 'error':
            assert False, self.cookie

    def upload(self, file):
        res = upload(self.cookie, file)
        if res == 'error':
            assert False, res
        else:
            return res


if __name__ == '__main__':
    pass
