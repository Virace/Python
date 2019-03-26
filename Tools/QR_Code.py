#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 20:19
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : QR_Code.py
# @Software: PyCharm

import qrcode
import zxing
import random
import os

from PIL import Image


def data_to_qrcode_png(data, file):
    # 实例化二维码生成类， border边框大小
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=1)
    # 设置二维码数据
    qr.add_data(data=data)

    qr.make(fit=True)

    # make_image这个位置可以设置二维码颜色，以及背景色
    qr.make_image().save(file)


def qrcode_to_data(filename):
    """
    二维码解析
    代码来源：https://www.cnblogs.com/zhongtang/p/7148375.html
    修改部分代码，子调用时会无法解析原因为zxing调用java包，需要考虑路径问题
    :param filename:
    :return:
    """
    img = Image.open(filename)
    ran = int(random.random() * 100000)
    img.save('%s%s.png' % (os.path.basename(filename).split('.')[0], ran))
    zx = zxing.BarCodeReader()

    zxdata = zx.decode('%s%s.png' % (os.path.basename(filename).split('.')[0], ran))
    # 删除临时文件
    os.remove('%s%s.png' % (os.path.basename(filename).split('.')[0], ran))
    if zxdata:
        return zxdata.parsed
    else:
        img.save('%s-zxing.png' % filename)


if __name__ == '__main__':
    pass
