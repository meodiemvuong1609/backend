from fastapi import FastAPI
from app.api.account import account_router
from app.api.auth import auth_router

app = FastAPI()

app.include_router(account_router)
app.include_router(auth_router)