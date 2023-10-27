from fastapi import Depends
from sqlalchemy.orm import Session

from app.models.models import Store
from app.database.schemas import StoreCreate, StoreUpdate
from app.database.session import get_session

from .base import BaseService

class StoresService(BaseService[Store, StoreCreate, StoreUpdate]):
    def __init__(self, db_session: Session):
        super(StoresService, self).__init__(Store, db_session)

def get_stores_service(db_session: Session = Depends(get_session)) -> StoresService:
    return StoresService(db_session)