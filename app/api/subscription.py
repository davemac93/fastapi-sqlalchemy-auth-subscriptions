from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from typing import Annotated

from app.core.database import get_db
from app.models.subscription import Subscription
from app.models.user import User
from app.api.dependecies import get_current_user

db_dependency = Annotated[Session, Depends(get_db) ]
user_dependency = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/api/subscription", tags=["subscriptions"])

@router.get('/')
async def get_all_sub(db: db_dependency):
    subscriptions = db.query(Subscription).all()

    for sub in subscriptions:
        print(f"ID: {sub.id}, Option: {sub.option}, Price: {sub.price}\n")

    return {"users": subscriptions}

@router.get("/my-subscription")
async def get_subscription(current_user: user_dependency, db: db_dependency):
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    return sub
