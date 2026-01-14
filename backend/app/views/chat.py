from fastapi import APIRouter, Depends, Path, Header, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import * # Изменимть на конкретные потом

import app.controllers.chat as chat_controller


router = APIRouter(prefix="/chat", tags=["Chats"])