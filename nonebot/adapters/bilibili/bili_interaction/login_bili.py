#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project :BiliInteraction 
@File    :login_bili.py
@Author  :Asadz
@Date    :2023/1/11 19:46 
"""
import httpx
from .. import utils


class Login:
    def __init__(self):
        self.client = httpx.Client(headers={
            'origin': 'https://live.bilibili.com',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        })

    def getQRcode(self):
        """
        在终端打印登录二维码
        :return:
        """
        getLoginQRApi = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header"
        qrData = self.client.get(getLoginQRApi).json()
        loginApi = qrData["data"]["url"]
        qrcodeKey = qrData["data"]["qrcode_key"]
        utils.printUrlQRcode(loginApi)
        return qrcodeKey

    def qrWaiting(self, qrcodeKey: str):
        """
        等待用户扫描二维码
        :param qrcodeKey: 二维码令牌
        :return: 用于验证csrf的数据
        """
        params: dict[str, str] = {
            "qrcode_key": qrcodeKey,
            "source": "main - fe - header",
        }
        waitApi: str = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
        issoSetApi = 'https://passport.bilibili.com/x/passport-login/web/sso/list?biliCSRF={}'
        while True:
            r = self.client.get(url=waitApi, params=params)
            if url := r.json()["data"]["url"]:
                self.client.get(url)
                break
        bili_jct = self.client.cookies.get("bili_jct")
        return bili_jct

    def completionCookie(self, jct: str):
        """
        登录后Cookie是不全的 这里补全Cookie
        :param jct: 登录返回的用于验证csrf的数据
        :return: None
        """
        ssoSetApi = f'https://passport.bilibili.com/x/passport-login/web/sso/list?biliCSRF={jct}'
        apis = self.client.get(ssoSetApi).json()["data"]["sso"]
        for url in apis:
            self.client.post(url)
