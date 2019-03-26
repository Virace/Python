#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 20:55
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : Watermark.py
# @Software: PyCharm


# 图片操作，水印


from PIL import Image


def add_watermark_by_img(img_file, wm_file, out_file):
    """
    给图片添加图片水印(默认局中)
    :param img_file: 图片路径
    :param wm_file: 水印图片路径
    :param out_file: 输出文件路径
    :return:
    """
    # 打开水印文件
    watermark = Image.open(wm_file)
    # 打开图片文件
    file = Image.open(img_file)
    # 创建输出文件
    layer = Image.new('RGBA', file.size, (0, 0, 0, 0))
    # 将水印图片“粘贴”在源图片上, 后面参数是粘贴位置，这个根据自己的水印图片操作，当前为横纵局中
    layer.paste(
        watermark,
        (
            file.size[0] // 2 - watermark.size[0] // 2,
            file.size[1] // 2 - watermark.size[1] // 2
        )
    )
    # 混合
    out = Image.composite(layer, file, layer)
    out.save(out_file)


if __name__ == '__main__':
    pass
