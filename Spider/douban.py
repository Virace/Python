#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/24 5:07
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : douban.py
# @Software: PyCharm


import json
import requests
from bs4 import BeautifulSoup


def get_item_name(obj):
    """
    取出字典中name值
    :param obj:
    :return:
    """
    return [item['name'] for item in obj]


def get_video_info(_id):
    """
    获取豆瓣信息，导演、编剧、演员、评分等
    :param _id:
    :return:
    """
    url = 'https://movie.douban.com/subject/{}/'.format(_id)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    source = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text(), strict=False)

    # 删除不必要信息
    source.pop('@context')
    source.pop('url')
    source.pop('duration')
    source.pop('@type')
    source['aggregateRating'].pop('@type')

    # 替换海报链接
    source['image'] = source['image'].replace('s_ratio_poster', 'r')
    # 将演员等信息格式化为列表
    source['director'] = get_item_name(source['director'])
    source['author'] = get_item_name(source['author'])
    source['actor'] = get_item_name(source['actor'])

    return source


def get_video_id_by_name(name):
    url = 'https://frodo.douban.com/api/v2/search/mix?' \
          'q={}' \
          '&type=movie' \
          '&apikey=0b2bdeda43b5688921839c8ecb20399b' \
          '&_sig=UjtMoOtFY0XatCAclg8wgDb8EOs%3D' \
          '&_ts=1553424800'.format(name)
    res = requests.get(url, headers={'user-agent': 'api-client/1 com.douban.movie/4.5.0(81)'})
    source = res.json()

    source = [item['items'] for item in source['modules'] if item['title'] == '影视']
    _id = source[0][0]['uri'].split('/')[-1]
    return _id


if __name__ == '__main__':
    _id = get_video_id_by_name('闪电侠第五季')
    print(_id)
    info = get_video_info(_id)
    print(info)
