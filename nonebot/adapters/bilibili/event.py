from copy import deepcopy
from typing_extensions import override
from typing import Dict, Any, List, Type, Literal


from pydantic import model_validator
from nonebot.adapters import Event as BaseEvent
from nonebot.compat import model_dump

from .message import Message


class Event(BaseEvent):

    @classmethod
    def new(cls, json_data: Dict):
        def all_subclasses(cls: Type[Event]):
            return set(cls.__subclasses__()).union(
                [s for c in cls.__subclasses__() for s in all_subclasses(c)])

        event_type = json_data["cmd"]
        all_event = all_subclasses(cls)
        event_class = None
        for event in all_event:
            if event.__name__ == event_type.capitalize():
                event_class = event
                break
        if event_class is None:
            return
        e = event_class.model_validate(json_data)
        return e

    @override
    def get_type(self) -> str:
        raise NotImplementedError

    @override
    def get_event_name(self) -> str:
        raise NotImplementedError

    @override
    def get_event_description(self) -> str:
        return str(model_dump(self))

    @override
    def get_message(self) -> Message:
        raise NotImplementedError

    @override
    def get_plaintext(self) -> str:
        raise NotImplementedError

    @override
    def get_user_id(self) -> str:
        raise NotImplementedError

    @override
    def get_session_id(self) -> str:
        raise NotImplementedError

    @override
    def is_tome(self) -> bool:
        return False

# 消息事件 -- 弹幕、醒目留言
class MessageEvent(Event):
    message: Message
    session_id: str

    @overrides(Event)
    def get_type(self):
        return 'message'

    @overrides(Event)
    def get_message(self):
        return self.message

    @overrides(Event)
    def get_session_id(self) -> str:
        return f'group_{self.session_id}'


class Danmu_msg(MessageEvent):
    """ 弹幕 """
    info: List[Any]

    @root_validator(pre=True, allow_reuse=True)
    def check_message(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["session_id"] = deepcopy(values["info"][9]["ct"])
        values["message"] = deepcopy(values['info'][1])
        return values

    @overrides(Event)
    def get_user_id(self) -> str:
        return str(self.info[2][0])

    def get_user_name(self) -> str:
        return self.info[2][1]


class Super_chat_message(MessageEvent):
    """ 醒目留言 """
    data: Dict[str, Any]
    duration: int

    @model_validator(pre=True, allow_reuse=True)
    def check_message(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["session_id"] = deepcopy(values["data"]["token"])
        values["massage"] = deepcopy(values["data"]["message"])
        values["duration"] = deepcopy(values["data"]["time"])
        return values

    @overrides(Event)
    def get_user_id(self) -> str:
        return str(self.data["uid"])


# 通知事件 -- 入房、开通舰长、礼物
class NoticeEvent(Event):

    @overrides(Event)
    def get_type(self) -> Literal["notice"]:
        return 'notice'


class Combo_send(NoticeEvent):
    """ 连击礼物 """
    data: Dict[Any, Any]


class Send_gift(NoticeEvent):
    """ 投喂礼物 """
    data: Dict[Any, Any]


class Common_notice_danmaku(NoticeEvent):
    """ 限时任务(系统通知的) """
    data: Dict[Any, Any]


class Entry_effect(NoticeEvent):
    """ 舰长进房 """
    data: Dict[Any, Any]


class Interact_word(NoticeEvent):
    """ 普通进房消息 """
    data: Dict[Any, Any]


class Guard_buy(NoticeEvent):
    """ 上舰 """
    data: Dict[Any, Any]


class User_toast_msg(NoticeEvent):
    """ 续费舰长 """
    data: Dict[Any, Any]


class Notice_msg(NoticeEvent):
    """ 在本房间续费了舰长 """
    id: int
    name: str
    full: Dict[str, Any]
    half: Dict[str, Any]
    side: Dict[str, Any]
    scatter: Dict[str, int]
    roomid: int
    real_roomid: int
    msg_common: int
    msg_self: str
    link_url: str
    msg_type: int
    shield_uid: int
    business_id: str
    marquee_id: str
    notice_type: int

    @overrides(Event)
    def get_event_name(self) -> str:
        return self.name


class Like_info_v3_click(NoticeEvent):
    """ 点赞 """
    data: Dict[Any, Any]


class Like_info_v3_update(NoticeEvent):
    """ 总点赞数 """
    data: Dict[Any, Any]


class Online_rank_count(NoticeEvent):
    """ 在线等级统计 """
    data: Dict[Any, Any]


class Online_rank_v2(NoticeEvent):
    """ 在线等级榜 """
    data: Dict[Any, Any]


class Popular_rank_changed(NoticeEvent):
    data: Dict[Any, Any]


class Room_change(Event):
    """ 房间信息变动(分区、标题等) """
    data: Dict[Any, Any]


class Room_real_time_message_update(NoticeEvent):
    """ 房间数据 """
    data: Dict[Any, Any]


class Watched_change(NoticeEvent):
    """ 直播间观看人数 """
    data: Dict[Any, Any]


class Stop_live_room_list(NoticeEvent):
    """ 下播列表 """
    data: Dict[Any, Any]
    room_id_list: List[int]

    @root_validator(pre=True, allow_reuse=True)
    def check_message(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["room_id_list"] = deepcopy(values["data"]["room_id_list"])
        return values


class Anchor_lot_start(NoticeEvent):
    """ 天选之人开始 """
    data: Dict[Any, Any]

    def get_anchor_lot_info(self):
        """ 获取天选之人的相关信息 """
        return {
            "award_name": self.data["award_name"],
            "danmu": self.data["danmu"],
            "gift_name": self.data["gift_name"]
        }


class Anchor_lot_award(NoticeEvent):
    """ 天选之人结果 """
    data: Dict[Any, Any]

    def winner_info(self):
        """ 获取中奖人信息 """
        return self.data["award_users"]