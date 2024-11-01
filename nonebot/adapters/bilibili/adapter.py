import asyncio
from typing import (
    Any,
    Dict,
    List,
)

from nonebot.adapters import Adapter as BaseAdapter
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    WebSocket,
    ForwardDriver,
)
from nonebot.message import handle_event
from nonebot.typing import overrides

from .bili_interaction import login as login_bilibili
from .bot import Bot
from .config import Config
from .event import Event
from .utils import rawData_to_jsonData, roomId_to_rawData, log,convert_cookies_to_dict

import httpx
import nonebot



class Adapter(BaseAdapter):

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "BilibiliLive"

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.bilibili_config: Config = Config(**self.config.dict())
        if self.bilibili_config.login:
            self.bili = login_bilibili()
            if not self.bilibili_config.cookies == "" :
                cookies:dict=convert_cookies_to_dict(self.bilibili_config.cookies)
                self.bili.cookies=httpx.Cookies()
                self.bili.cookies.clear()
                for k,v in cookies.items():
                    self.bili.cookies.set(name=k,value=v)
                self.bili.jcr=cookies.get("bili_jct")
                log("INFO",f"ID: {self.bili.cookies.get('DedeUserID')} login successful")
            else: 
                log("WARNING","cookie没有配置，将采用二维码登录")
                self.bili.login()
                log("INFO",f"ID: {self.bili.cookies.get('DedeUserID')} login successful")
                
            
        self.connections: Dict[str, WebSocket] = {}
        self.tasks: List['asyncio.Task'] = []
        self._setup()
    def _setup(self) -> None:
        if isinstance(self.driver, ForwardDriver):
            self.driver.on_startup(self.start_ws_client)
            self.driver.on_shutdown(self.stop_ws_client)
        else:
            log.error(f"{self.get_name()} 请添加 websockets 和 httpx 驱动以使用本 adapter")

    async def start_ws_client(self):
        for room_id in self.bilibili_config.room_id_list:
            self.tasks.append(asyncio.create_task(self._client(room_id)))

    async def stop_ws_client(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def _client(self, room_id):
        request = Request(
            "GET",
            URL("wss://broadcastlv.chat.bilibili.com/sub"),
            headers={
                "Origin": "https://live.bilibili.com",
                "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
                "Sec-WebSocket-Version": "13",
                "Upgrade": "websocket",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"
            },
            timeout=30
        )
        while True:
            try:
                async with self.websocket(request) as ws:
                    await ws.send_bytes(bytes.fromhex(roomId_to_rawData(room_id)))
                    log("DEBUG",
                        f"[{room_id}] Successfully joined room {room_id}"
                        )
                    self.tasks.append(t := asyncio.create_task(self.sendHB(ws, room_id)))
                    bot = Bot(self, room_id)
                    self.bot_connect(bot)
                    self.connections[room_id] = ws
                    while True:
                        if ws.closed:
                            self.bot_disconnect(bot)
                            self.tasks.remove(t)
                            log(
                                "WARNING",
                                "Lost connection, try to reconnect"
                            )
                            continue
                        data = await ws.receive_bytes()
                        json_data = rawData_to_jsonData(data)
                        if json_data is None:
                            continue
                        else:
                            event_class = Event.new(json_data)
                            if event_class is None:
                                continue
                            asyncio.create_task(handle_event(
                                bot,
                                event_class
                            ))
            except Exception as e:
                self.bot_disconnect(bot)
                self.tasks.remove(t)
                log(
                    "ERROR",
                    f"Error connecting websocket, ERROR: {e}"
                )
            await asyncio.sleep(3)

    async def sendHB(self, ws, room_id):
        hb = "0000001f0010000100000002000000015b6f626a656374204f626a6563745d"
        while True:
            await asyncio.sleep(29)
            await ws.send_bytes(bytes.fromhex(hb))
            if ws.closed:
                return
            log(
                "DEBUG",
                f"[{room_id}] send HB"
            )

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        log(
            "DEBUG",
            "ppp"
        )
