from pydantic import BaseModel

class AuthLogin(BaseModel):
  username: str
  password: str
