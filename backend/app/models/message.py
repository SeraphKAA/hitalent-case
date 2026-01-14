from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column( # возможно уберу
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Связь с чатом
    chat: Mapped["ChatModel"] = relationship(  # type: ignore
        "ChatModel", back_populates="messages"
    )

    def __repr__(self):
        return f"<Message(id={self.id}, chat_id={self.chat_id})>"
