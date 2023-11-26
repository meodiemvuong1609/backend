from pydantic import BaseModel

class ChatRoomBase(BaseModel):
  title: str
  type: str = "PRIVATE"

class ChatRoomCreate(ChatRoomBase):
  title: str
  type: str = "PRIVATE"
  account: list
  