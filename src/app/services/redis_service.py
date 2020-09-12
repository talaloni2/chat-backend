from enum import Enum
from typing import TypeVar, Type, NamedTuple, Optional, List, Any, Union, Iterable

from pydantic import parse_obj_as, BaseModel
from redis import Redis

ModelT = TypeVar('ModelT')


class RedisService(NamedTuple):

    redis: Redis

    def get(self, key: Any, as_model: Type[ModelT]) -> Optional[ModelT]:
        value = self.redis.get(key)
        if value is None:
            return None

        return parse_obj_as(as_model, value)

    def lrange(
            self,
            key: Any,
            start: int,
            end: int,
            node_model: Type[ModelT]
    ) -> Optional[List[ModelT]]:
        values = self.redis.lrange(key, start, end)

        if values is None:
            return None

        return parse_obj_as(List[node_model], values)

    def hset(self, hash_key: str, field: str, value: Union[str, bytes, Enum, BaseModel]):

        set_value = None

        if isinstance(value, Enum):
            set_value = str(value.value)
        elif isinstance(value, bytes):
            set_value = value
        elif isinstance(value, str):
            set_value = value
        elif isinstance(value, BaseModel):
            set_value = value.json()
        else:
            raise ValueError(
                f"value must be either str, bytes, Enum or pydantic BaseModel, was {type(value)}")

        self.redis.hset(hash_key, field, set_value)

    def scan_iter(self, prefix, batch_size: int = 100) -> Iterable:
        return self.redis.scan_iter(f'{prefix}*', count=batch_size)

    def keys_exists(self, *keys):
        return self.redis.exists(*keys)
