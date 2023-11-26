from fastapi import APIRouter
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.general.base import *
from app.database.session import get_session
from app.models.chat import ChatRoom, ChatRoomAccount
from app.basemodels.chat import ChatRoomCreate
chat_router = APIRouter()


@chat_router.get("/chat/api/chatroom/")
def account_get_chatroom(request: Request, current_user: Account = Depends(get_current_user), db: Session = Depends(get_db)):
  chatrooms = db.query(ChatRoom).join(ChatRoomAccount).filter(ChatRoomAccount.account_id == current_user.id).all()
  return convert_response("Success", 200, [chatroom.to_dict() for chatroom in chatrooms])

@chat_router.post("/chat/api/chatroom/")
def account_create_chatroom(chatroom: ChatRoomCreate, current_user: Account = Depends(get_current_user), db: Session = Depends(get_db)):
  chatroom_db = ChatRoom(
    title=chatroom.title,
    user_created=current_user.id
  )
  try:
    db.add(chatroom_db)
    db.commit()
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