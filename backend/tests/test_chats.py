import pytest
from datetime import datetime
from unittest.mock import AsyncMock

import app.controllers.chat as chat_controller
import app.controllers.message as message_controller


@pytest.mark.asyncio
async def test_create_chat(client, mock_session, monkeypatch):
    chat = {
        "id": 1,
        "title": "Test chat",
        "created_at": datetime.utcnow(),
    }

    monkeypatch.setattr(
        chat_controller,
        "create_chat",
        AsyncMock(return_value=chat),
    )

    response = await client.post(
        "/chats/",
        json={"title": "Test chat"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test chat"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_chat_title_too_long(client):
    long_title = "a" * 201  # > 200 символов

    response = await client.post(
        "/chats/",
        json={"title": long_title},
    )

    assert response.status_code == 422

    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_create_message_text_too_long(client):
    long_text = "a" * 5001  # > 5000 символов

    response = await client.post(
        "/chats/1/messages",
        json={"text": long_text},
    )

    assert response.status_code == 422

    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_get_all_chats(client, monkeypatch):
    chats = [
        {"id": 1, "title": "Chat 1", "created_at": datetime.utcnow()},
        {"id": 2, "title": "Chat 2", "created_at": datetime.utcnow()},
    ]

    monkeypatch.setattr(
        chat_controller,
        "get_chats",
        AsyncMock(return_value=chats),
    )

    response = await client.get("/chats/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Chat 1"


@pytest.mark.asyncio
async def test_create_message(client, monkeypatch):
    message = {
        "id": 1,
        "chat_id": 10,
        "text": "Hello",
        "created_at": datetime.utcnow(),
    }

    monkeypatch.setattr(
        message_controller,
        "create_message",
        AsyncMock(return_value=message),
    )

    response = await client.post(
        "/chats/10/messages",
        json={"text": "Hello"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == 10
    assert data["text"] == "Hello"


@pytest.mark.asyncio
async def test_get_chat_with_messages(client, monkeypatch):
    result = {
        "chat": {
            "id": 1,
            "title": "Chat",
            "created_at": datetime.utcnow(),
        },
        "messages": [
            {
                "id": 1,
                "chat_id": 1,
                "text": "Hi",
                "created_at": datetime.utcnow(),
            }
        ],
    }

    monkeypatch.setattr(
        chat_controller,
        "get_chat_with_messages",
        AsyncMock(return_value=result),
    )

    response = await client.get("/chats/1?limit=10")

    assert response.status_code == 200
    data = response.json()
    assert data["chat"]["id"] == 1
    assert len(data["messages"]) == 1


@pytest.mark.asyncio
async def test_delete_chat(client, monkeypatch):
    monkeypatch.setattr(
        chat_controller,
        "delete_chat",
        AsyncMock(return_value=None),
    )

    response = await client.delete("/chats/1")

    assert response.status_code == 204
