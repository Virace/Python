#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/24 20:05
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : tvmaze.py
# @Software: PyCharm

import requests


def get_video_info_by_name(name):
    """
    根据影片名(英文)获取影片信息
    :param name:
    :return:
    """
    url = 'http://api.tvmaze.com/search/shows?q={}'.format(name)
    res = requests.get(url)
    source = res.json()

    source = source[0]['show']

    source.pop('url')
    source.pop('type')
    source.pop('genres')
    source.pop('runtime')
    source.pop('officialSite')
    source.pop('weight')
    source.pop('webChannel')
    source.pop('summary')
    source.pop('updated')
    source.pop('_links')

    return source


if __name__ == '__main__':
    info = get_video_info_by_name('the flash')
    print(info)
