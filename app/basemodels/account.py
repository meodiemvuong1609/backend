from typing import Optional
from pydantic import BaseModel


class AccountBase(BaseModel):
  username: Optional[int]
  password: Optional[int]
  email: Optional[int]
  fullname: Optional[int] = None
class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    id: Optional[int]

class AccountDelete(BaseModel):
    id: Optional[int]