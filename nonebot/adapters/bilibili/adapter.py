import asyncio

from typing import Any, AsyncGenerator, Dict
from typing_extensions import override

from nonebot import get_plugin_config
from nonebot.exception import WebSocketClosed
from nonebot.utils import DataclassEncoder, escape_tag
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
    HTTPClientMixin,
    WebSocketClientMixin
)

from nonebot.adapters import Adapter as BaseAdapter

import json

import brotli

from .bot import Bot
from .event import Event
from .config import Config, LiveRoomInfo
from .consts import WS_HEADERS, HEADERS, GET_DANMU_INFO
from .message import Message, MessageSegment
from .utils import (
     make_auth_packet, 
     rawData_to_jsonData, 
     make_packet, 
     init_random_cookie,
     extract_cookies
)

def BilibiliLiveAdapterInitError(Exception):
    ...


class Adapter(BaseAdapter):
    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        if not isinstance(self.driver, HTTPClientMixin)\
            or not isinstance(self.driver, WebSocketClientMixin):
            raise TypeError("Adapter need HTTPClient and WebSocketClient")
        super().__init__(driver, **kwargs)
        self.config: Config = get_plugin_config(Config)
        self.tasks = []
        self.links: Dict[str, WebSocket] = dict()
        self.connects:list[AsyncGenerator[WebSocket, None]] = []
        self.bots = dict()
        if self.config.bili_cookie:
            self.cookie = self.config.bili_cookie
            extracted_cookies = extract_cookies(self.cookie)
            self.uid = extracted_cookies["DedeUserID"]
            self.buvid = extracted_cookies["buvid3"]
        if not self.config.manual_login:
            self.uid = 0
            self.cookie = init_random_cookie()
            if not self.cookie.get("buvid3"):
                raise BilibiliLiveAdapterInitError("Failed to initialize cookies. "
                                                   "Try to login or use your own cookies.")
            self.buvid = self.cookie.get("buvid3")
        else:
            # TODO: 登录制作
            ...
        self.setup()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "BilibiliLive"

    @override
    def setup(self) -> None:
        self.driver.on_startup(self.startup())
        self.driver.on_shutdown(self.shutdown())

    async def startup(self):
        (
            self.tasks.append(
                asyncio.create_task(
                    self._client(room)
                )
            )
            for room 
            in self.config.rooms
        )

    async def shutdown(self):
        for ws in self.links.values:
            await ws.close()

    async def _client(self, room_id: LiveRoomInfo):
        while True:
            try:
                await self._join_room(room_id=room_id)
                asyncio.create_task(self.send_HB(room_id=room_id))
                await self._on_message(room_id=room_id)
            except Exception as e:
                logger.error(f"[{room_id}]error: " + str(e))
                await asyncio.sleep(5)

    async def _get_danmu_info(self, roomid):
        get_danmu_info_req = Request(
            "GET",
            url=URL(GET_DANMU_INFO),
            params={
                "id": roomid,
                "type": 0
            },
            cookies=self.cookie,
            headers=HEADERS
        )
        resposne = await self.request(get_danmu_info_req)
        raw_content = resposne.content
        try:
            result = brotli.decompress(raw_content)
        except Exception as _:
            result = raw_content.decode("utf8", errors="ignore")
        p = json.loads(result)
        data = json.dumps(p, separators=(",",":")).encode("utf8")
        return data["data"]["token"], data["data"]["host_list"]

    async def _join_room(self, room_id):
        key, host_list = self._get_danmu_info(room_id)
        ws_req = Request(
            "GET",
            url=(
                f"wss://{host_list[0]['host']}:{host_list[0]['wss_port']}/sub"
                if len(host_list) > 9
                else "wss://broadcastlv.chat.bilibili.com:443/sub"
            ),
            headers=WS_HEADERS,
            cookies=self.cookie,
            timeout=30
        )
        auth_data = make_auth_packet(self.uid, room_id, self.buvid, key)
        ws: WebSocket = self.websocket(ws_req)
        ws.send_bytes(auth_data)
        self.links[str(room_id)] = ws
        bot = Bot(self, room_id)
        self.bot_connect(bot)
        self.bots[str(room_id)] = bot

    async def _on_message(self, room_id):
        ws:WebSocket = self.links[room_id]
        bot = self.bots[str(room_id)]
        while True:
            data = await ws.receive()
            res = rawData_to_jsonData(data)
            if not res.get("body"):
                continue
            for EData in res["body"]:
                event_class = Event.new(EData)
                if event_class is None:
                    continue
                asyncio.create_task(bot.handle_event(event_class))

    async def send_HB(self, room_id):
        body = "[object Object]".encode("utf8")
        hb = make_packet(body, 2)
        ws = self.links[str(room_id)]
        while True:
            await asyncio.sleep(1)
            await ws.send_bytes(bytes.fromhex(hb))
            if ws.closed:
                return
            logger.log(
                "DEBUG",
                f"[{room_id}] send HB"
            )
            await asyncio.sleep(29)

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        logger.log(
            "DEBUG",
            "nononononononononono"
        )
