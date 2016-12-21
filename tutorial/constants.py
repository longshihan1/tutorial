#!/usr/bin/python
# -*- coding: utf-8 -*-


from tutorial.settings import USER_AGENT

HEADER = {
    'Host': 'www.zhihu.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': '*/*',
    'Origin': 'https://www.zhihu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': USER_AGENT,
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
}
