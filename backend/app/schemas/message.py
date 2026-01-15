from pydantic import BaseModel, StringConstraints
from datetime import datetime
from typing_extensions import Annotated

from app.models import MessageModel


class MessageCreateDto(BaseModel):
    text: Annotated[str, StringConstraints(min_length=1, max_length=5000)]


class MessageOutDto(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    @staticmethod
    def new(message: MessageModel):
        return MessageOutDto(
            id=message.id,
            chat_id=message.chat_id,
            text=message.text,
            created_at=message.created_at,
        )
