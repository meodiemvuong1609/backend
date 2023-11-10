from fastapi import APIRouter
from app.general.base import *
from app.database.session import get_session
from app.models.chat import ChatRoom, ChatRoomAccount, ChatMessage
from app.basemodels.chat import ChatRoomCreate

chat_router = APIRouter()

@chat_router.get("/chat/api/chatroom/")
@is_authenticated
def account_get_chatroom(request: Request):
  session = get_session()
  chatrooms = session.query(ChatRoom).join(ChatRoomAccount).filter(ChatRoomAccount.account_id == request.user_id).all()
  return convert_response("Success", 200, [chatroom.to_dict() for chatroom in chatrooms])

@chat_router.post("/chat/api/chatroom/")
@is_authenticated
def account_create_chatroom(request: Request, chatroom: ChatRoomCreate):
  session = get_session()
  chatroom_db = ChatRoom(
    name=chatroom.title,
    user_created=request.user_id
  )
  try:
    session.add(chatroom_db)
    session.commit()

    chatroom_accounts_db = [ChatRoomAccount(
      chatroom_id=chatroom_db.id,
      account_id=account
    ) for account in chatroom.account]
    session.bulk_save_objects(chatroom_accounts_db)
    session.commit()
  except:
    session.rollback()
    return convert_response("Error", 400)
  return convert_response("Success", 200)