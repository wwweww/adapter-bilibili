from struct import Struct

HEADERS = headers = {
"accept": "*/*",
"accept-encoding": "gzip, deflate, br, zstd",
"accept-language": "zh-CN,zh;q=0.9",
"cache-control": "no-cache",
"origin": "https://live.bilibili.com",
"pragma": "no-cache",
"priority": "u=1, i",
"referer": "https://live.bilibili.com",
"sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "\"Windows\"",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-site",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

WS_HEADERS = {
    "host": "broadcastlv.chat.bilibili.com",
    "origin": "https://live.bilibili.com",
    "pragma": "no-cache",
    "sec-websocket-extensions": "permessage-deflate; client_max_window_bits",
    "sec-websocket-version": "13",
    "upgrade": "websocket",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

GET_DANMU_INFO = "https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo"

HEADER_STRUCT = Struct(">I2H2I")

SEND_API = "https://api.live.bilibili.com/msg/send"