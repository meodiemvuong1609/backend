from fastapi import WebSocket, WebSocketDisconnect, Depends
from fastapi.routing import APIRouter
from app.general.base import *
from app.models.chat import ChatMessage, ChatRoomAccount
from app.models.account import Account
import json
from datetime import datetime

account_socket_router = APIRouter()

class ConnectionManager:
  def __init__(self):
    self.active_connections = []
    self.rooms = []
  

  def db_sync_message(self, room_id: int, userId: int, message: str, db=get_session()):
    chat_message = ChatMessage(
      chatroom=room_id,
      account=userId,
      message=message,
      created_at=datetime.now()
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message

  async def connect(self, websocket: WebSocket, user_id: int):
    await websocket.accept()
    self.active_connections.append({"user_id": user_id, "websocket": websocket})
  async def disconnect(self, websocket: WebSocket, user_id: int):
    await websocket.close()
    self.active_connections.remove({"user_id": user_id, "websocket": websocket})

  async def send_message_to_room(self, data: dict):
    try:
      roomId = data["roomId"]
      message = data["message"]
      userList = data["userList"]
      userId = data["userId"]
      for connection in self.active_connections:
        if connection["user_id"] in userList:
          try:
            await connection["websocket"].send_json({
            "message": message,
            "account": userId,
            "chatroom": roomId,
            "type": "chat_message"
          })
          except Exception as e:
            print(e)
            self.active_connections.remove(connection)
            print(self.active_connections)
      self.db_sync_message(roomId, userId, message)
    except Exception as e:
      print(e)

manager = ConnectionManager()
@account_socket_router.websocket("/ws/{user_id}/")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
  await manager.connect(websocket, user_id)
  try:
    while True:
      data = await websocket.receive_text()
      data = json.loads(data)
      await manager.send_message_to_room(data)
  except WebSocketDisconnect:
    await manager.disconnect(websocket, user_id)