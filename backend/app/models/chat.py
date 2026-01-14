from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base


class ChatModel(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Связь 1-N с сообщениями
    messages: Mapped[list["MessageModel"]] = relationship(  # type: ignore
        "MessageModel", back_populates="chat", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Chat(id={self.id}, title='{self.title}')>"
