#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project :BiliInteraction 
@File    :interaction.py
@Author  :Asadz
@Date    :2023/1/11 19:45 
"""
import httpx
from .login_bili import Login

class BilibiliDriver(Login):
    def __init__(self):
        super().__init__()
        self.cookies = None
        self.jcr = None

    def login(self):
        qrcodeKey = self.getQRcode()
        self.jcr = self.qrWaiting(qrcodeKey)
        self.completionCookie(self.jcr)
        self.cookies = self.client.cookies

    async def send(self, msg, room_id):
        sendApi = "https://api.live.bilibili.com/msg/send"
        async with httpx.AsyncClient(cookies=self.cookies, headers=self.client.headers) as aclient:
            data = {'bubble': '0',
                    'msg': msg,
                    'color': '16777215',
                    'mode': '1',
                    'fontsize': '25',
                    'rnd': '1673365377',
                    'roomid': str(room_id),
                    'csrf': self.jcr,
                    'csrf_token': self.jcr,
                    }
            await aclient.post(sendApi, data=data)


def login():
    return BilibiliDriver()
