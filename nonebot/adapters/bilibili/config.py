from pydantic import Field, BaseModel


class LiveRoomInfo(BaseModel):
    """ 直播间id """
    room_id: str = "1331407"


class Config(BaseModel):
    """ 用户cookie可有可无 没有的话就看不见用户信息 """
    bili_cookie: str = "None"
    rooms: list[str]
    manual_login: bool = False