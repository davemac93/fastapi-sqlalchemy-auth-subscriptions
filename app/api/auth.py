from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import timedelta

from app.core.database import get_db
from app.core.security import PasswordManager, TokenManager
from app.core.config import settings
from app.models import User, Subscription
from app.schemas import CreateUser
from app.api.dependecies import get_current_user


router = APIRouter(prefix="/api/auth", tags=["users"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: db_dependency):
    existing_user = db.query(User).filter(
        or_(User.email == user.email, User.username == user.username)
    ).first()
    if existing_user:
        detail = "Email already registered" if existing_user.email == user.email else "Username already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
            )
    try:
        hashedpassword = PasswordManager.hash_password(user.password)

        new_user = User(
            username= user.username,
            email= user.email,
            hashed_password= hashedpassword
        )

        db.add(new_user)
        db.flush()

        new_subscription = Subscription(
            user_id = new_user.id,
        )

        db.add(new_subscription)

        db.commit()
        db.refresh(new_user)
        return {"messsage": f"{user.username} created!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, details="An error occured creating the account")

@router.post("/signin", status_code=status.HTTP_200_OK)
async def login_user(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = PasswordManager.authenticate_user(user_data.username, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        token = TokenManager.create_access_token(
            user.username, 
            user.id, 
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error generating the access token"
        )

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_details(current_user: user_dependency):

    return {
        "username": current_user.username,
        "email": current_user.email,
        "id": current_user.id
    }

@router.get("/users")
async def get_all_users(db: db_dependency):
    users = db.query(User).all()
    for user in users:
        print(f"Email: {user.email}, Username: {user.username}\n")
    return {"users": users}