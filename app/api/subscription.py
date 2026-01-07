from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from typing import Annotated

from app.core.database import get_db
from app.models.subscription import Subscription

db_dependency = Annotated[Session, Depends(get_db) ]

router = APIRouter(prefix="/api/subscriptions", tags=["users"])

@router.get('/')
async def get_all_sub(db: db_dependency):
    subscriptions = db.query(Subscription).all()

    for sub in subscriptions:
        print(f"ID: {sub.id}, Option: {sub.option}, Price: {sub.price}\n")

    return {"users": subscriptions}

    
