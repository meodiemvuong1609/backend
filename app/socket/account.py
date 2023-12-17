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
  
  async def addOnlineUser(self, user_id: int, db=get_session()):
    account = db.query(Account).filter(Account.id == user_id).first()
    account.is_online = True
    db.commit()
    db.refresh(account)
    return account

  def db_sync_message(self, message: dict, room_id: str, db=get_session()):
    chat_message = ChatMessage(
      chatroom=room_id,
      account=message["userId"],
      message=message["message"],
      created_at=datetime.now()
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message

  async def connect(self, websocket: WebSocket, user_id: int):
    try:
      await websocket.accept()
      self.active_connections.append({"user_id": user_id, "websocket": websocket})
      await self.addOnlineUser(user_id)

      await self.send_online_users()
    except:
      pass
  async def disconnect(self, websocket: WebSocket, user_id: int):
    try:
      self.active_connections.remove({"user_id": user_id, "websocket": websocket})
      await self.send_online_users()
    except:
      pass

  async def send_online_users(self, db=get_session()):
    online_users = db.query(Account).filter(Account.is_online == True).all()
    message = {"action": "onlineUser", "userList": [user.id for user in online_users]}
    for connection in self.active_connections:
      await connection["websocket"].send_json(message)

  async def send_message(self, message: dict, room_id: str):
    for connection in self.active_connections:
      await connection["websocket"].send_json({"type": "chat_message", "message": message})
  async def send_message_to_room(self, message: dict, room_id: str):
    await self.send_message(message, room_id)
    self.db_sync_message(message, room_id)
manager = ConnectionManager()
@account_socket_router.websocket("/ws/{user_id}/")
async def websocket_endpoint(websocket: WebSocket, user_id: int, ):
  await manager.connect(websocket, user_id)
  try:
    while True:
      data = await websocket.receive_text()
      message = json.loads(data)
      await manager.send_message_to_room(message, message["roomId"])
  except WebSocketDisconnect:
    pass
    # manager.disconnect(websocket, user_id)