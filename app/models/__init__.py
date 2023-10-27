from typing import Any
from sqlalchemy.ext.declarative import declarative_base
from .account import Account
from .chat import ChatRoom, ChatRoomAccount, ChatMessage
Base: Any = declarative_base()
