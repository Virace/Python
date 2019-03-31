#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/30 16:54
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : adb.py
# @Software: PyCharm
# adb安卓操作

import os


class Adb(object):
    """
    命令中默认使用了 root 权限，如果不需要则 shell 直接加命令即可 不需要su -c""
    """
    # adb.exe 执行文件
    adb_path = r".\adb.exe"

    def tap(self, x, y):
        """
        点击
        :param x:
        :param y:
        :return:
        """
        adb_command = 'input tap {} {}'.format(x, y)
        cmd_command = '{} shell su -c "{}"'.format(self.adb_path, adb_command)
        os.system(cmd_command)

    def input(self, text):
        """
        输入文本
        :param text:
        :return:
        """
        adb_command = 'input text {}'.format(str(text))
        cmd_command = '{} shell su -c "{}"'.format(self.adb_path, adb_command)
        os.system(cmd_command)

    def swipe(self, old, new):
        """
        滑动从坐标old(x,y),滑动到new(x,y)
        :param old:
        :param new:
        :return:
        """
        adb_command = 'input swipe {} {} {} {}'.format(*old, *new)
        cmd_command = '{} shell su -c "{}"'.format(self.adb_path, adb_command)
        os.system(cmd_command)

    def screen(self, out):
        """
        截图并输出
        :param out:
        :return:
        """
        adb_command = '/system/bin/screencap -p /sdcard/screenshot.png'
        cmd_command = '{} shell su -c "{}"'.format(self.adb_path, adb_command)
        os.system(cmd_command)
        adb_command = 'pull /sdcard/screenshot.png {}'.format(out)
        cmd_command = '{} {}'.format(self.adb_path, adb_command)
        os.system(cmd_command)


if __name__ == '__main__':
    pass
