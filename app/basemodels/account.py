from typing import Optional
from pydantic import BaseModel


class AccountBase(BaseModel):
  username: Optional[str]
  password: Optional[str]
  email: Optional[str]
  fullname: Optional[str] = None
class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    id: Optional[int]

class AccountDelete(BaseModel):
    id: Optional[int]