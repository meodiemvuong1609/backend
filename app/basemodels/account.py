from pydantic import BaseModel


class AccountBase(BaseModel):
  username: str
  password: str
  email: str
  fullname: str = None
