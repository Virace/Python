#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 3:50
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : sohuTV.py
# @Software: PyCharm

# 使用模块前请注意错误处理！！！！！

import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import requests


def download_sohu_video_parts(_id, out_path):
    """
    根据视频ID下载视频
    :param _id: ID可以在网页源码中找到
    :param out_path: 保存目录
    :return: 返回分段视频文件路径列表
    """

    url1 = 'https://hot.vrs.sohu.com/vrs_flash.action?vid={}'.format(_id)

    url2 = 'https://vipbjyz.vod.tv.itc.cn/ip?new={}'

    # 获取分段视频
    res1 = requests.get(url1)
    data1 = res1.json().get('data')
    paths = data1.get('su')
    if paths:
        i = 1
        items = list()
        for path in paths:
            print('当前下载:第{}段,共{}段'.format(i, len(paths)))
            # 下载分段视频
            res2 = requests.get(url2.format(path))
            vidoe_url = res2.json().get('servers')[0].get('url')
            res3 = requests.get(vidoe_url, stream=True)
            path = os.path.join(out_path, "%d.mp4" % i)
            f = open(path, "wb")
            # chunk是指定每次写入的大小，每次只写了512byte
            for chunk in res3.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            f.close()
            # 将分段视频文件路径加入列表
            items.append(path)
            i += 1
        return items


def merge_video(video_list, output_file, del_temp=True):
    """
    合并视频
    :param video_list: 分段视频列表
    :param output_file: 输出文件路径
    :param del_temp: 是否删除分段视频
    :return:
    """
    # 实测没有直接调用ffmpeg concat处理速度快，因为这个需要重新编码
    # 并没有实际去细究moviepy模块，只是完成功能
    videos = [VideoFileClip(item) for item in video_list]
    final_clip = concatenate_videoclips(videos)
    final_clip.to_videofile(output_file)
    if del_temp:
        for item in video_list:
            os.remove(item)


if __name__ == '__main__':
    pass
