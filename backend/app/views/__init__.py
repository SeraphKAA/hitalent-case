from fastapi import APIRouter
from . import chat, message

api_router = APIRouter()

api_router.include_router(chat.router)
api_router.include_router(message.router)