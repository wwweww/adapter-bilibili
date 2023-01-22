import asyncio
from typing import (
    Any,
    Union,
)

from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides

from .event import Event
from .message import Message, MessageSegment


class Bot(BaseBot):

    @overrides(BaseBot)
    async def send(
            self,
            event: Event,
            message: Union[str, Message, MessageSegment],
            **kwargs,
    ) -> Any:
        asyncio.create_task(self.adapter.bili.send(message, self.self_id))
