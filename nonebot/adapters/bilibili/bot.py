from typing import Union, Any
from typing_extensions import override

from nonebot.adapters import Bot as BaseBot
from nonebot.drivers import Request, URL

from .event import Event
from .message import Message, MessageSegment
from .consts import HEADERS, SEND_API

class Bot(BaseBot):

    @override
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs,
    ) -> Any:
        self.adapter.request(
            Request(
                "POST",
                url=URL(SEND_API),
                headers=HEADERS,
                data={
                    "bubble": "0",
                    "msg": str(message),
                    "color": "16777215",
                    "mode": "1",
                    "room_type": "0",
                    "jumpfrom": "0",
                    "reply_mid": "0",
                    "reply_attr": "0",
                    "replay_dmid": "",
                    "statistics": "{\"appId\":100,\"platform\":5}",
                    "reply_type": "0",
                    "reply_uname": "",
                    "fontsize": "25",
                    "rnd": "1730528504",
                    "roomid": "1331407",
                    "csrf": "16549f1988456afa8043b52abfc1b682",
                    "csrf_token": "16549f1988456afa8043b52abfc1b682"
                },
                cookies=self.adapter.cookie
            )
        )
