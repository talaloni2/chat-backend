from typing import NamedTuple, List, Optional

from app.model.message import MessageModel
from app.services.redis_naming import room_key, room_messages
from app.services.redis_service import RedisService
from base64 import urlsafe_b64encode
from uuid import uuid4 as uuid

ROOM_NAME_FIELD = 'name'
ROOM_ICON_FIELD = 'icon'
ROOM_MESSAGES_FIELD = 'messages'
# WE NEED THE HASH FOR ROOM KEY SORT
ROOMS_HASH_KEY = 'rooms'


class RoomService(NamedTuple):

    redis_service: RedisService

    def get_latest_messages(self, room_id, amount: int):
        return self.redis_service.lrange(room_key(room_id), amount*-1, -1, MessageModel)

    def generate_room(self, name: str, icon_path: str) -> str:
        room_id = self.generate_room_id()
        key = room_key(room_id)
        self.redis_service.hset(key, ROOM_NAME_FIELD, name)
        self.redis_service.hset(key, ROOM_ICON_FIELD, icon_path)
        self.redis_service.hset(key, ROOM_MESSAGES_FIELD, room_messages(room_id))
        return room_id

    def generate_room_id(self):
        return urlsafe_b64encode(uuid().bytes).strip(b'=').decode('utf-8')
