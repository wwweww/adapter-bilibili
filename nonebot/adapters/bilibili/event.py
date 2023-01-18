import dataclasses
from abc import ABC
from typing import Dict, Any

from nonebot.typing import overrides
from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent

from .message import Message


class Event(BaseEvent):
    """
    使用bilibili websocket不同的消息类型(cmd)作为事件类型
    -哔哩哔哩直播弹幕 Websocket 协议参考: https://github.com/lovelyyoshino/Bilibili-Live-API/blob/master/API.WebSocket.md-
    """
    cmd: str

    @classmethod
    def new(cls, json_data: Dict):
        event_type = json_data["cmd"]
        all_event = cls.__subclasses__()
        event_class = None
        for event in all_event:
            if event.__name__ == event_type.capitalize():
                event_class = event
                break
        return event_class.parse_obj(json_data)

    def get_type(self) -> str:
        return self.cmd

    def get_event_name(self) -> str:
        return self.cmd

    def get_event_description(self) -> str:
        return str(self.dict())

    def get_message(self) -> Message:
        raise NotImplementedError

    def get_plaintext(self) -> str:
        raise NotImplementedError

    def get_user_id(self) -> str:
        raise NotImplementedError

    def get_session_id(self) -> str:
        raise NotImplementedError

    def is_tome(self) -> bool:
        return False


class Combo_send(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Combo_send'

class Common_notice_danmaku(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Common_notice_danmaku'


class Danmu_msg(Event):
    info: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Danmu_msg'


class Entry_effect(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Entry_effect'


class Guard_buy(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Guard_buy'


class Interact_word(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Interact_word'


class Like_info_v3_click(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Like_info_v3_click'


class Like_info_v3_update(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Like_info_v3_update'


class Notice_msg(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Notice_msg'


class Online_rank_count(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Online_rank_count'


class Online_rank_v2(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Online_rank_v2'


class Popular_rank_changed(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Popular_rank_changed'


class Room_change(Event):
    data: Dict[Any, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'Room_change'


class Interact_word(Event):
    data: Dict[Any, Any]


class Interact_word(Event):
    data: Dict[Any, Any]
