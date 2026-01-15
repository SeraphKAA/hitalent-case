from pydantic import BaseModel, StringConstraints
from typing import List
from datetime import datetime
from typing_extensions import Annotated

from app.models import ChatModel, MessageModel
from .message import MessageOutDto, MessageCreateDto


class ChatCreateDto(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=200)]


class ChatOutDto(BaseModel):
    id: int
    title: str
    created_at: datetime

    @staticmethod
    def new(chat: ChatModel):
        return ChatOutDto(
            id=chat.id,
            title=chat.title,
            created_at=chat.created_at,
        )


class ChatWithMessagesDto(BaseModel):
    chat: ChatOutDto
    messages: List[MessageOutDto]

    @staticmethod
    def new(chat: ChatModel, messages: list[MessageModel]):
        return ChatWithMessagesDto(
            chat=ChatOutDto.new(chat),
            messages=[MessageOutDto.new(msg) for msg in messages],
        )
