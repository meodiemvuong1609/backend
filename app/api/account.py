from fastapi import APIRouter
from app.general.base import *
from app.database.session import get_session
from app.basemodels.account import AccountBase
from app.models.account import Account

account_router = APIRouter()

@account_router.post("/account/api/register/")
def account_register(account: AccountBase):
  session = get_session()
  account_db = Account(
    username=account.username,
    password=oauth2.get_password_hash(account.password),
    email=account.email,
    fullname=account.fullname,
    is_active=True,
    is_online=False
  )
  try:
    session.add(account_db)
    session.commit()
    return convert_response("Success", 200)
  except:
    session.rollback()
    return convert_response("Error", 400)
  finally:
    session.close()
