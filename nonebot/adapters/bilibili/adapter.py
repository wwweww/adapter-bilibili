import asyncio
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Union,
    Callable,
    Optional,
    AsyncGenerator,
)

from nonebot.typing import overrides
from nonebot.exception import WebSocketClosed
from nonebot.utils import DataclassEncoder, escape_tag
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
)

from nonebot.adapters import Adapter as BaseAdapter

from .bot import Bot
from .event import Event
from .config import Config
from .message import Message, MessageSegment

from .utils import rawData_to_jsonData, roomId_to_rawData, log
from .bili_interaction import login as login_bilibili


class Adapter(BaseAdapter):

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "BilibiliLive"

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        # self.bili = login_bilibili()
        # log(
        #     "INFO",
        #     f"ID: {self.bili.cookies.get('DedeUserID')} login successful"
        # )
        self.bilibili_config: Config = Config(**self.config.dict())
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
                "Upgrade": "websocket"
            },
            timeout=30.0
        )
        while True:
            try:
                async with self.websocket(request) as ws:
                    await ws.send(bytes.fromhex(roomId_to_rawData(room_id)))  # 进房
                    log("DEBUG",
                        f"Successfully joined room {room_id}"
                        )
                    await asyncio.gather(asyncio.create_task(self.sendHB(ws)),  # 心跳包
                                         asyncio.create_task(self.ws_event(ws, room_id))  # 事件处理
                                         )
            except ConnectionRefusedError as e:
                log.warn(f"connection error ({room_id}):{e} ")
                break
            await asyncio.sleep(3)

    async def ws_event(self, ws: WebSocket, room_id: str):
        bot = Bot(self, room_id)
        self.bot_connect(bot)
        self.connections[room_id] = ws
        while True:
            raw_data = await ws.receive()
            json_data = rawData_to_jsonData(raw_data)
            log(
                "DEBUG",
                json_data
            )
            if ws.closed:
                log(
                    "WARNING",
                    "Websocket is disconnected, try to reconnect."
                )
                await self.ws_event(ws, room_id)

    async def sendHB(self, ws):
        hb = "00000010001000010000000200000001"
        while True:
            await asyncio.sleep(30)
            await ws.send(bytes.fromhex(hb))

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        log(
            "DEBUG",
            "ppp"
        )
