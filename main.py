from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.account import account_router
from app.api.auth import auth_router
from app.api.chat import chat_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router)
app.include_router(auth_router)
app.include_router(chat_router)
