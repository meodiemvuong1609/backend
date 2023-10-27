from fastapi import APIRouter
from app.database.session import get_session
from app.models import Account
auth_router = APIRouter()

@auth_router.post("/account/login")
def account_login(username: str, password: str):
    session = get_session()
    user = session.query(Account).filter(Account.username == username).first()
    if user is None:
        return {"message": "User not found"}


    return {"message": "Login"}