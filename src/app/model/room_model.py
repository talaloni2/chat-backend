from typing import List

from app.model.base_model import JsonBaseModel
from app.model.message import MessageModel


class RoomListViewModelNode(JsonBaseModel):
    id: str
    name: str
    icon_path: str


class RoomSingleViewModel(JsonBaseModel):
    id: str
    name: str
    icon_path: str
    messages: List[MessageModel]
