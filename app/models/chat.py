import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.models.account import Base

class ChatRoomAccount(Base):
    __tablename__ = 'chat_chatroomaccount'
    
    id              = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    chatroom_id     = sa.Column(sa.Integer, ForeignKey('chat_chatroom.id'), primary_key=True)
    account_id      = sa.Column(sa.Integer, ForeignKey('account_account.id'), primary_key=True)

class ChatRoom(Base):
    __tablename__   = "chat_chatroom"

    id              = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title           = sa.Column(sa.String(50), nullable=False)
    type            = sa.Column(sa.String(10), nullable=False, default="PRIVATE")
    user_created    = sa.Column(sa.Integer, ForeignKey('account_account.id'), nullable=False)
    member          = relationship("Account", secondary="chat_chatroomaccount", back_populates="chat_rooms")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "user_created": self.user_created,
        }
class ChatMessage(Base):
    __tablename__   = "chat_chatmessage"
    id              = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    chatroom        = sa.Column(sa.Integer, ForeignKey('chat_chatroom.id'), nullable=False)
    account         = sa.Column(sa.Integer, ForeignKey('account_account.id'), nullable=False)
    message         = sa.Column(sa.Text, nullable=False)
    created_at      = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)



