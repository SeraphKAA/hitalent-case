from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import (
    MessageCreateDto,
    MessageOutDto,
    ChatCreateDto,
    ChatOutDto,
    ChatWithMessagesDto,
)
import app.controllers.chat as chat_controller
import app.controllers.message as message_controller
from app.database.database import get_db

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/", response_model=ChatOutDto, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreateDto, session: AsyncSession = Depends(get_db)
):
    """Создание чата"""
    return await chat_controller.create_chat(chat_data, session)


@router.get("/", response_model=list[ChatOutDto])
async def get_all_chats(session: AsyncSession = Depends(get_db)):
    """Получение всех чатов"""
    return await chat_controller.get_chats(session)


@router.post("/{chat_id}/messages", response_model=MessageOutDto)
async def create_message(
    chat_id: int,
    message_data: MessageCreateDto,
    session: AsyncSession = Depends(get_db),
):
    """Создание сообщения в чат по id чата"""
    return await message_controller.create_message(chat_id, message_data, session)


@router.get("/{chat_id}", response_model=ChatWithMessagesDto)
async def get_chat_with_messages(
    chat_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    """Получение n сообщений (стандарт: 20) по id чата"""
    return await chat_controller.get_chat_with_messages(chat_id, limit, session)


@router.delete("/{chat_id}", status_code=204)
async def delete_chat(chat_id: int, session: AsyncSession = Depends(get_db)):
    """Удаление чата"""
    await chat_controller.delete_chat(chat_id, session)
