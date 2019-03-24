#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/24 22:45
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @File    : wp_rest_api.py
# @Software: PyCharm
# https://developer.wordpress.org/rest-api
# 自用
import requests


class Wordpress(object):
    def __init__(self):
        # 管理员账户密码
        data = {
            'username': 'xxx',
            'password': 'xxx'
        }
        # 获取登录token
        rq = requests.post('https://xxx.xxx/wp-json/jwt-auth/v1/token', json=data)
        rq.encoding = 'utf-8-sig'
        result = rq.json()
        if 'token' in result.keys():
            token = result['token']
            self.headers = {'Authorization': 'Bearer ' + token}
        else:
            print(result['code'])

            assert False, '登录出错'

    def edit_post(self, pid, data):
        """
        编辑文章
        :param pid:
        :param data:data https://developer.wordpress.org/rest-api/reference/posts/
        :return:
        """
        api = 'https://xxx.xxx/wp-json/wp/v2/posts/' + pid
        rq = requests.post(api, json=data, headers=self.headers)
        rq.encoding = 'utf-8-sig'
        return rq.json()

    def get_post(self, pid):
        """
        获取文章信息
        :param pid:
        :return:
        """
        api = 'https://xxx.xxx/wp-json/wp/v2/posts/' + pid
        rq = requests.get(api, headers=self.headers)
        rq.encoding = 'utf-8-sig'
        return rq.json()


if __name__ == '__main__':
    pass
