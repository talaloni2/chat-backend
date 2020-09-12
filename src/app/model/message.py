from app.model.base_model import JsonBaseModel


class MessageModel(JsonBaseModel):
    message: str
    user_id: int
