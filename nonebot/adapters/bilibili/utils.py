#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project :nonebotAdapterTest 
@File    :utils.py
@Author  :Asadz
@Date    :2023/1/11 18:01 
"""
import os
import json
import zlib

import pickle

from qrcode_terminal import draw
from nonebot.utils import logger_wrapper
import qrcode

log = logger_wrapper("BilibiliLive")


def roomId_to_rawData(roomId):
    a = '{"roomid":' + str(roomId) + '}'
    data = []
    for s in a:
        data.append(ord(s))
    return "000000{}001000010000000700000001".format(hex(16 + len(data))[2:]) + "".join(
        map(lambda x: x[2:], map(hex, data)))


def rawData_to_jsonData(data: bytes):
    packetLen = int(data[:4].hex(), 16)
    ver = int(data[6:8].hex(), 16)
    op = int(data[8:12].hex(), 16)

    if len(data) > packetLen:  # 防止
        rawData_to_jsonData(data[packetLen:])
        data = data[:packetLen]

    if ver == 2:
        data = zlib.decompress(data[16:])
        return rawData_to_jsonData(data)

    if op == 5:
        try:
            jd = json.loads(data[16:].decode('utf-8', errors='ignore'))
            return jd
        except Exception as e:
            pass


def printUrlQRcode(url: str):
    """
    连接转换二维码 终端输出
    :param url: 链接
    :return:
    """
    # draw(url)
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.print_ascii(invert=True)


def saveCookies(cookies):
    """
    保存cookie
    :param cookies: cookie对象
    :return:
    """
    if "config" not in os.listdir():
        os.mkdir("config")

    with open("./config/config.pickle", "wb") as cookieFile:
        pickle.dump(cookies, cookieFile)


def loadCookie():
    """
    导入cookie
    :return: cookie对象
    """
    if "config" not in os.listdir():
        return
    with open("./config/config.pickle", "rb") as cookieFile:
        return pickle.load(cookieFile)
