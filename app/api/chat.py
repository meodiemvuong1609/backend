from fastapi import APIRouter
from fastapi import Depends, Request
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy import desc
from app.general.base import *
from app.database.session import get_session
from app.models.chat import ChatRoom, ChatRoomAccount, ChatMessage
from app.basemodels.chat import ChatRoomCreate
chat_router = APIRouter()


@chat_router.get("/chat/api/chatroom/")
def account_get_chatroom(request: Request, current_user: Account = Depends(get_current_user), db: Session = Depends(get_db)):
  chat_rooms = current_user.chat_rooms
  return chat_rooms

@chat_router.get("/chat/api/chatroom/{chatroom_id}/")
def account_get_chatroom(request: Request, chatroom_id: int, current_user: Account = Depends(get_current_user), db: Session = Depends(get_db)):
  chatroom = db.query(ChatRoom).join(ChatRoomAccount, chatroom_id==ChatRoomAccount.chatroom_id).first()

  if chatroom is None:
    raise HTTPException(status_code=404, detail="Chatroom not found")
  response = {
    "id": chatroom.id,
    "title": chatroom.title,
    "type": chatroom.type,
    "user_created": chatroom.user_created,
    "member": [{
      "id": member.id,
      "email": member.email,
      "fullname": member.fullname,
      "is_online": member.is_online
    
    } for member in chatroom.member]
  }
  return response

@chat_router.post("/chat/api/chatroom/")
def account_create_chatroom(chatroom: ChatRoomCreate, current_user: Account = Depends(get_current_user), db: Session = Depends(get_db)):
  chatroom_db = ChatRoom(
    title=chatroom.title,
    user_created=current_user.id
  )
  try:
    db.add(chatroom_db)
    db.commit()
    chatroom.account.append(current_user.id)
    chatroom_accounts_db = [ChatRoomAccount(
      chatroom_id=chatroom_db.id,
      account_id=account
    ) for account in chatroom.account]
    db.bulk_save_objects(chatroom_accounts_db)
    db.commit()
  except Exception as e:
    db.rollback()
    return convert_response(e, 400)
  return convert_response("Success", 200)

@chat_router.get("/chat/api/chatroommessage/{chatroom_id}/")
def get_chat_message(chatroom_id, current_user: Account = Depends(get_current_user), db: Session = Depends(get_db)):
  chatmessage = (db.query(ChatMessage).join(Account, ChatMessage.chatroom==chatroom_id).order_by(desc("created_at")).all())
  return chatmessage