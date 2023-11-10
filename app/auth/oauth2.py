from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

class OAuth2:
    def __init__(self, secret_key: str, algorithm: str, access_token_expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def _create_token(self, payload: dict, expires_delta: timedelta):
        to_encode = payload.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire.timestamp()})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_access_refresh_token(self, data: dict):
        # Create Acces Token
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self._create_token(data, access_token_expires)

        # Create Refresh Token
        refresh_token_expires = timedelta(days=30)
        refresh_token = self._create_token(data, refresh_token_expires)

        return access_token, refresh_token

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return False

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)