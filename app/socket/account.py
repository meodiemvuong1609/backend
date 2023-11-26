from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
from app.general.base import *
from app.models.chat import ChatMessage, ChatRoomAccount
from app.models.account import Account

account_socket_router = APIRouter()

class ConnectionManager:
  def __init__(self):
    self.connections = {}

  async def connect(self, user_id: int, websocket: WebSocket):
    await websocket.accept()
    if user_id in self.connections:
      self.connections[user_id].append(websocket)
    else:
      self.connections[user_id] = [websocket]

  def disconnect(self, user_id: int, websocket: WebSocket):
    if user_id in self.connections:
      self.connections[user_id].remove(websocket)
      if not self.connections[user_id]:
        del self.connections[user_id]

manager = ConnectionManager()

# WebSocket route to handle connections

@account_socket_router.websocket("/ws/{user_id}/")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
  await manager.connect(user_id, websocket)
  try:
    while True:
      db.query(Account).filter(Account.id == user_id).update({Account.is_online: True})
      db.commit()
  except WebSocketDisconnect:
    manager.disconnect(user_id, websocket)
    db.query(Account).filter(Account.id == user_id).update({Account.is_online: False})
    await websocket.close()

async def broadcast_message(user_id: int, message: str):
  if user_id in manager.connections:
    for connection in manager.connections[user_id]:
      await connection.send_text(message)

@account_socket_router.websocket("/ws/{user_id}/{chatroom_id}/")
async def chat_endpoint(websocket: WebSocket, user_id: int, chatroom_id: int, db: Session = Depends(get_db)):
  await manager.connect(user_id, websocket)
  try:
    while True:
      data = await websocket.receive_text()
      # Save the chat message to the database
      message = ChatMessage(chatroom=chatroom_id, account=user_id, message=data)
      db.add(message)
      db.commit()
      # Broadcast the message to all members of the chat room
      members = (
        db.query(ChatRoomAccount)
        .filter(ChatRoomAccount.chatroom_id == chatroom_id)
        .all()
      )
      for member in members:
        if member.account_id != user_id:
          await broadcast_message(member.account_id, data)
  except WebSocketDisconnect:
      manager.disconnect(user_id, websocket)