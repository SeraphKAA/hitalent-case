from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import MessageOutDto, MessageCreateDto
import app.controllers.message as message_controller
from app.database.database import get_db


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/", response_model=list[MessageOutDto])
async def get_all_messages(session: AsyncSession = Depends(get_db)):
    """Эндпоинт для проверки каскадного удаления (на всякий случай)"""
    return await message_controller.get_all_messages(session)


@router.patch("/change", response_model=MessageOutDto)
async def change_message_text(
    message_id: int,
    message_data: MessageCreateDto,
    session: AsyncSession = Depends(get_db),
):
    """Изменение комментария по Id комментария"""
    return await message_controller.change_message_text(
        message_id, message_data, session
    )
