#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 18:35
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : 163Musci.py
# @Software: PyCharm

# 该接口只能下载 128kbs


import os
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/74.0.3702.0 Safari/537.36'}


def get_playlist(pid):
    """
    根据歌单ID获取歌单所有歌曲ID和歌曲名称列表
    :param pid:
    :return:格式为[(歌曲id1, 歌曲名称1), (歌曲id2, 歌曲名称2), .......]
    """

    res = requests.get('https://music.163.com/playlist?id={}'.format(pid), headers=headers)
    source = res.text
    soup = BeautifulSoup(source, 'lxml')
    ul = soup.select('#song-list-pre-cache ul li')
    songs = list()
    for item in ul:
        _id = item.select_one('a')['href'].split('=')[-1]
        # print(item.string, item.select_one('a')['href'])
        songs.append((_id, item.string))
    return songs


def download_music_by_id(item, out_path):
    """
    下载歌曲
    :param item: 格式为(歌曲id, 歌曲名称)
    :param out_path:
    :return:
    """
    url = 'http://music.163.com/song/media/outer/url?id={}'.format(item[0])
    res = requests.get(url, headers=headers)
    f = open(os.path.join(out_path, item[1] + '.mp3'), "wb")
    # chunk是指定每次写入的大小，每次只写了512byte
    for chunk in res.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()


def search_music(name):
    """
    根据歌曲名字获取歌曲信息
    :param name:
    :return: id、name、 picUrl、song  ，歌曲id 、歌曲名称、歌曲封面、 歌曲下载地址
    """
    url = 'http://s.music.163.com/search/get/?version=1&src=lofter&type=1&s={}'.format(name)
    res = requests.get(url)
    source = res.json()
    if source['code'] == 200:
        source = source['result']['songs']
        result = list()
        for item in source:
            result.append({
                'id': item['id'],
                'name': '{} - {}'.format(item['name'], '、'.join([i['name'] for i in item['artists']])),
                'picUrl': item['album']['picUrl'],
                'song': item['audio']
            })
        return result


if __name__ == '__main__':
    pass
