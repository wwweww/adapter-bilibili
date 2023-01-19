from typing import Union, Mapping, Iterable, Type
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment
from nonebot.typing import overrides


class MessageSegment(BaseMessageSegment):

    def __str__(self) -> str:
        return self.data["msg"]

    def __add__(self, other) -> "Message":
        return Message(self) + other

    def __radd__(self, other) -> "Message":
        return Message(other) + self

    def is_text(self) -> bool:
        return self.type == "danmu"

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @staticmethod
    def danmu(msg: str):
        return MessageSegment("danmu", {"msg": msg})


class Message(BaseMessage):

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str):
        yield MessageSegment.danmu(msg)
