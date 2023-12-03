from app.models.account import Account
from fastapi import HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from app.auth.oauth2 import OAuth2
from sqlalchemy.orm import Session
from app.database.session import get_session
oauth2 = OAuth2("secret_key", "HS256", 300)
from app import crud
def convert_response(message, status_code, data=None, count=None):
  """
    Convert body response to normalization.
  """
  
  response = {
    "message": message,
    "code": status_code,
  }
  
  if data is not None:
    response.update({"data": data})
  if count is not None:
    response.update({"count": count})

  return response

def get_db():
  db = get_session()
  try:
    yield db
  finally:
    db.close()

def get_current_user(request: Request, db: Session = Depends(get_db))->Account:
  access_token = request.cookies.get("access_token")
  if access_token is None:
    raise HTTPException(detail="Missing access token", status_code=400)
  payload = oauth2.verify_token(access_token)
  if not payload:
    raise HTTPException(detail="Invalid access token", status_code=400)
  account_id = payload["sub"]
  account = crud.account.get_by_id(db, id=account_id)
  return account
