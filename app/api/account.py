from fastapi import APIRouter
from app.general.base import *
from app.database.session import get_session
from app.basemodels.account import AccountBase
from app.models.account import Account

account_router = APIRouter()

@account_router.get("/account/api/me/")
async def account_get_me(request: Request, db: Session = Depends(get_db), current_user: Account = Depends(get_current_user)):
  user = current_user
  return user.to_dict()

@account_router.get("/account/api/account/")
async def account_list_account(request: Request, db: Session = Depends(get_db), current_user: Account = Depends(get_current_user)):
  accounts = db.query(Account).all()
  return convert_response("Success", 200, [account.to_dict() for account in accounts])

@account_router.post("/account/api/register/")
def account_register(account: AccountBase, db: Session = Depends(get_db)):
  account_db = Account(
    username=account.username,
    password=oauth2.get_password_hash(account.password),
    email=account.email,
    fullname=account.fullname,
    is_active=True,
    is_online=False
  )
  try:
    db.add(account_db)
    db.commit()
    return convert_response("Success", 200)
  except:
    db.rollback()
    return convert_response("Error", 400)