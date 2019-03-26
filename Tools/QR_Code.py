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
from pyzbar import pyzbar


def data_to_qrcode_png(data, file, version=None, box_size=10, border=4):
    # 实例化二维码生成类， border边框大小
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        version=version,
        box_size=box_size,
        border=border
    )
    # 设置二维码数据
    qr.add_data(data=data)

    qr.make(fit=True)

    # make_image这个位置可以设置二维码颜色，以及背景色
    # 这里如果需要后续修改图片建议 转为RGBA 如果不修改默认为1 二值图像
    # 如果make_image 修改背景或二维码颜色 就不用转换，也就是可以去掉convert函数
    qr.make_image().convert("RGBA").save(file)


def qrcode_to_data(filename):
    """
    二维码解析
    代码来源：https://www.cnblogs.com/zhongtang/p/7148375.html
    修改部分代码，子调用时会无法解析原因为zxing调用java包，需要考虑路径问题
    :param filename:
    :return:
    """
    img = Image.open(filename)
    # 先用pyzbar包解析，如果解析不成功则用zxing模块解析
    data = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
    if data:
        return data[0].data.decode('utf-8')
    else:
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
