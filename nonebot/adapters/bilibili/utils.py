import json
import re
from typing import Union
from .consts import HEADER_STRUCT, HEADERS
from .types import HeaderTuple

from nonebot.log import logger 

import brotli
import httpx

class PacketOffset:
    WS_PACKAGE_OFFSET = slice(0, 4)
    WS_HEADER_OFFSET = slice(4, 2)
    WS_VERSION_OFFSET = slice(6, 2)
    WS_OPERATION_OFFSET = slice(8, 2)
    WS_SEQUENCE_OFFSET = slice(12, 4)
    U32 = lambda s=0: slice(s, s+4)
    U16 = lambda s=0: slice(s, s+2)
    WS_BINARY_HEADER_LIST = [
        {
            "name": "Header Length",
            "key": "headerLen",
            "offset": WS_HEADER_OFFSET,
        },
        {
            "name": "Protocol Version",
            "key": "ver",
            "offset": WS_VERSION_OFFSET,
        },
        {
            "name": "Operation",
            "key": "op",
            "offset": WS_OPERATION_OFFSET,
        },
        {
            "name": "Sequence Id",
            "key": "seq",
            "offset": WS_SEQUENCE_OFFSET,
        }
    ] 


def make_packet(data: Union[dict, str, bytes],
                operation: int):
    if isinstance(data, dict):
        body = json.dumps(data, separators=(",",":")).encode("utf8")
    elif isinstance(data, str):
        body = data.encode("utf8")
    else:
        body = data
    header = HEADER_STRUCT.pack(*HeaderTuple(
        pack_len=HEADER_STRUCT.size + len(body),
        raw_header_size=HEADER_STRUCT.size,
        ver=1,
        operation=operation,
        seq_id=1
    ))

    return header + body


def make_auth_packet(uid, room_id, buvid3, key):
    auth_params = {
        'uid': int(uid),
        'roomid': int(room_id),
        'protover': 3,
        'buvid': buvid3,
        'platform': 'web',
        'type': 2,
        'key': key
    }
    return make_packet(auth_params, 7)


def rawData_to_jsonData(data: bytes):
    packetLen = int(data[PacketOffset.WS_PACKAGE_OFFSET].hex(), 16)
    result = dict()
    result["body"] = []

    for e in PacketOffset.WS_BINARY_HEADER_LIST:
        result[e["key"]] = int(data[e['offset']].hex(), 16)

    if (packetLen < len(data)):
        return rawData_to_jsonData(data[:packetLen])
    if (result["op"] and result["op"] == 3):
        result["body"] = {"count": int(data[PacketOffset.U32(16)].hex(), 16)}
    else:
        n = 0
        s = packetLen
        a = ""
        l = ""
        while n < len(data):
            s = int(data[PacketOffset.U32(n)].hex(), 16)
            a = int(data[PacketOffset.U16(n+4)].hex(), 16)
            try:
                if(result["ver"] == 3):
                    h = data[n+a:n+s]
                    l = brotli.decompress(h).decode("utf8", errors="ignore")
                elif (result["ver"] == 0 or result["ver"] == 1):
                    l = data.decode("utf8", errors="ignore")
                l = json.loads(l[l.index("{"):])
                result["body"].append(l)
            except Exception as e:
                logger.error("数据解析失败", e)

            n += s
    return result


def init_random_cookie():
    with httpx.Client(headers=HEADERS) as client:
        client.get("https://www.bilibili.com/")
    return client.cookies


def extract_cookies(cookie_string):
    pattern = r'(?P<name>buvid3|DedeUserID)=(?P<value>[^;]+)'
    matches = re.findall(pattern, cookie_string)

    cookie_dict = {name: value for name, value in matches}
    return cookie_dict

def get_room_id(room):
        with httpx.Client(headers=HEADERS) as client:
            resp = client.get("https://live.bilibili.com/1576468")
        res = resp.text
        pattern = r'"room_id":(\d{3,})'
        r = re.findall(pattern, res)
        if r:
            return r[0]
        else:
            raise Exception("Failed to get real room number")