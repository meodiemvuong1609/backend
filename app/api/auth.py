from fastapi import APIRouter, Response
from app.database.session import get_session
from app.models.account import Account
from app.general.base import *
from app.basemodels.auth import AuthLogin

auth_router = APIRouter()

@auth_router.post("/auth/api/login/")
def account_login(auth: AuthLogin, response: Response):
  session = get_session()
  user = session.query(Account).filter(Account.username == auth.username).first()
  if user is None:
    return convert_response("Invalid usename", 400)
  if not oauth2.verify_password(auth.password, user.password):
    return convert_response("Invalid password", 400)
  access_token, refresh_token = oauth2.create_access_refresh_token(data={"sub": str(user.id)})
  # set cookie for client
  response.set_cookie("access_token", access_token, httponly=True, max_age=oauth2.access_token_expire_minutes * 60)
  response.set_cookie("refresh_token", refresh_token, httponly=True)
  
  return convert_response("Success", 200, {"access_token": access_token, "refresh_token": refresh_token})

