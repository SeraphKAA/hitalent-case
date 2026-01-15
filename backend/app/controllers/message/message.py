from fastapi import HTTPException
from app.models import ChatModel, MessageModel
from app.schemas.chat import (
    MessageCreateDto,
    MessageOutDto,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


async def create_message(
    chat_id: int, dto: MessageCreateDto, session: AsyncSession
) -> MessageOutDto:
    query = select(ChatModel).where(ChatModel.id == chat_id)
    result = await session.execute(query)
    chat = result.scalar_one_or_none()

    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    text = dto.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Сообщение не может быть пустым")

    new_message: MessageModel = MessageModel(chat=chat, text=text)

    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)

    return MessageOutDto.new(new_message)


async def get_all_messages(session: AsyncSession) -> list[MessageOutDto]:
    query = select(MessageModel)
    result = await session.execute(query)
    messages = result.scalars().all()

    return [MessageOutDto.new(message) for message in messages]


async def change_message_text(
    message_id: int, dto: MessageCreateDto, session: AsyncSession
) -> MessageOutDto:
    query = select(MessageModel).where(MessageModel.id == message_id)
    result = await session.execute(query)
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Сообщения не найдено")

    message.text = dto.text
    await session.commit()
    await session.refresh(message)
    return MessageOutDto.new(message)
