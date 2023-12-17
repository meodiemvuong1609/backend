import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
  __tablename__   = "account_account"

  id              = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  username        = sa.Column(sa.String(50), unique=True, nullable=False)
  email           = sa.Column(sa.String(100), nullable=False)
  password        = sa.Column(sa.String(100), nullable=False)
  fullname        = sa.Column(sa.String(100), nullable=True)
  is_active       = sa.Column(sa.Boolean, default=True)
  is_online       = sa.Column(sa.Boolean, default=False)

  chat_rooms      = relationship("ChatRoom", secondary="chat_chatroomaccount", back_populates="member")

  def to_dict(self):
    return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "fullname": self.fullname,
        "is_active": self.is_active,
        "is_online": self.is_online
    }

