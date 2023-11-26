from typing import Optional
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from app.models.account import Account
from app.basemodels.account import AccountCreate, AccountUpdate, AccountDelete
from app.crud.base import CRUDBase


meta = MetaData()

class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> Optional[Account]:
        return db.query(Account).filter(Account.id == id).first()

account = CRUDAccount(Account)