#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/24 21:34
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : ImgUpload.py
# @Software: PyCharm

import os
import requests

from requests_toolbelt import MultipartEncoder


def upload_img(file):
    """
    上传图片至微博图传
    :param file:
    :return:
    """
    if os.path.isfile(file):
        # API : https://img.yyhyo.com/api.php
        url = 'https://img.yyhyo.com/upload.php?type=Sina'
        # 拼接提交数据
        multipart_encoder = MultipartEncoder(fields={
            # 测试中文文件名会有问题，所以只加上扩展名
            'fileupload': ('xx.' + file.split('.')[-1], open(file, 'rb'))
        })
        res = requests.post(url, data=multipart_encoder, headers={'Content-Type': multipart_encoder.content_type})
        source = res.json()
        if source['code'] == '0':
            return source['msg']


if __name__ == '__main__':
    pass
