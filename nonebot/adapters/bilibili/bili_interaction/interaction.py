#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project :BiliInteraction 
@File    :interaction.py
@Author  :Asadz
@Date    :2023/1/11 19:45 
"""
import httpx
from .login_bili import *


class BilibiliDriver:
    def __init__(self):
        self.login()
        self.cookies = None
        self.jcr = None

    def login(self):
        qrcodeKey = getQRcode()
        self.jcr = qrWaiting(qrcodeKey)
        completionCookie(self.jcr)
        self.cookies = client.cookies

    async def send(self, msg):
        sendApi = "https://api.live.bilibili.com/msg/send"
        async with httpx.AsyncClient(cookies=self.cookies, headers=client.headers) as aclient:
            data = {'bubble': '0',
                    'msg': msg,
                    'color': '16777215',
                    'mode': '1',
                    'fontsize': '25',
                    'rnd': '1673365377',
                    'roomid': '1331407',
                    'csrf': self.jcr,
                    'csrf_token': self.jcr,
                    }
            await aclient.post(sendApi, data=data)


def login():
    return BilibiliDriver()
