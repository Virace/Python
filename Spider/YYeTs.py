#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/24 3:26
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : YYeTs.py
# @Software: PyCharm


import requests


def get_video_info(_id):
    # 获取影片信息，rid为影片ID
    url = 'http://a.allappapi.com/index.php?' \
          'accesskey=519f9cab85c8059d17544947k361a827' \
          '&g=api%2Fv2' \
          '&a=resource' \
          '&rid={}'.format(_id)

    res = requests.get(url)
    source = res.json()
    source = source['data']
    source.pop('similar')
    source.pop('comments_hot')
    source.pop('share_url')
    source.pop('comments_count')
    source.pop('trailers')
    source['resource'].pop('score_counts')
    source['resource'].pop('rank')
    source['resource'].pop('favorites')
    source['resource'].pop('views')
    source['resource'].pop('format')
    source['resource'].pop('migu_music')
    source['resource'].pop('migu_h5')
    source['resource'].pop('poster')
    source['resource'].pop('poster_b')
    source['resource'].pop('poster_m')
    source['resource'].pop('poster_s')
    source['resource'].pop('level')
    source['resource'].pop('prevue')
    source['resource'].pop('prevue_list')

    return source


def get_file_item_magnet(obj):
    """
    从地址列表中获取对应链接
    :param obj:
    :return:
    """
    for item in obj:
        if item['way'] == '2':
            # 磁力链接
            return item['address'].split('&')[0]
        elif item['way'] == '102':
            # 百度云盘，拼接密码
            return '%s#%s' % (item['address'], item['passwd'])
        elif item['way'] == '115':
            # 微云
            return item['address']


def get_video_item_info(_id, season, episode):
    # 获取单集资源，id为影片ID,season为季,episode为集
    url = 'http://a.allappapi.com/index.php?' \
          'accesskey=519f9cab85c8059d17544947k361a827' \
          '&g=api/v2' \
          '&a=resource_item' \
          '&id={}' \
          '&season={}' \
          '&episode={}'.format(_id, season, episode)
    res = requests.get(url)
    source = res.json()
    # 精简json
    source = source['data']
    source.pop('item_app')
    source.pop('recommend_source')
    res = dict()
    res['sub'] = dict()
    res['unsub'] = dict()
    # 格式化无字幕与有字幕资源
    for item in source['item_list']:
        if item['format_tip'] == '无字幕版本':
            # 无字幕
            res['unsub'][item['foramt']] = get_file_item_magnet(item['files'])
        else:
            # 有字幕
            res['sub'][item['foramt']] = get_file_item_magnet(item['files'])

    for item in source['play_source']:
        res['sub'][item['way_cn']] = get_file_item_magnet(source['play_source'])

    return res


if __name__ == '__main__':
    print(get_video_info('32235'))
    print(get_video_item_info('32235', 5, 1))
