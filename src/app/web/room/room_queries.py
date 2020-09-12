from fastapi import Query

from app.model.room_model import RoomListViewModelNode
from src.app.web.room.router import router


@router.get('/rooms', response_model=RoomListViewModelNode)
def list_rooms(
        prefix: str = Query(default='', alias='q'),
        page: int = 1,
        size: int = 20,
):

