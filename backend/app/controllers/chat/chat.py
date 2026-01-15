from app.models import ChatModel, MessageModel
from app.schemas.chat import (
    MessageCreateDto,
    MessageOutDto,
    ChatCreateDto,
    ChatOutDto,
    ChatWithMessagesDto,
)

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


async def create_chat(dto: ChatCreateDto, session: AsyncSession) -> ChatOutDto:
    title = dto.title.strip()

    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Заголовок не может быть пустым",
        )

    if len(title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Заголовок не должен превышать 200 симоволов",
        )

    new_chat = ChatModel(title=title)
    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)

    return ChatOutDto.new(new_chat)


async def get_chats(session: AsyncSession) -> list[ChatOutDto]:
    query = select(ChatModel)
    result = await session.execute(query)
    chats = result.scalars().all()

    return [ChatOutDto.new(chat) for chat in chats]


async def get_chat_with_messages(
    chat_id: int, limit: int, session: AsyncSession
) -> ChatWithMessagesDto:
    query = select(ChatModel).where(ChatModel.id == chat_id)
    result = await session.execute(query)
    chat = result.scalar_one_or_none()

    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    query = (
        select(MessageModel)
        .where(MessageModel.chat_id == chat_id)
        .order_by(desc(MessageModel.created_at))
        .limit(limit)
    )

    result = await session.execute(query)
    messages = result.scalars().all()

    messages = list(reversed(messages))  # изменение порядка сообщений по времени от новых к старым

    return ChatWithMessagesDto.new(chat, messages)


async def delete_chat(chat_id: int, session: AsyncSession) -> None:
    query = select(ChatModel).where(ChatModel.id == chat_id)
    result = await session.execute(query)
    chat = result.scalar_one_or_none()

    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    await session.delete(chat)
    await session.commit()
