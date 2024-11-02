from typing import Type, Union, Mapping, Iterable
from typing_extensions import override

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):

    @classmethod
    @override
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @override
    def __str__(self) -> str:
        return self.data["body"]

    @override
    def is_text(self) -> bool:
        return self.type == "danmu"


    @staticmethod
    def danmu(msg: str):
        return MessageSegment("danmu", {"msg": msg})


class Message(BaseMessage[MessageSegment]):

    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        raise NotImplementedError
