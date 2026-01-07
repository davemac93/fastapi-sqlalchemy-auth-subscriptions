from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import or_

from app.core import settings
from app.models import User

class PasswordManager:
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.bcrypt_context.hash(password)
    @classmethod
    def verified_password(cls, password: str, hashedpassword: str) -> bool:
        return cls.bcrypt_context.verify(password, hashedpassword)

    @classmethod
    def authenticate_user(cls, username_or_email: str, password: str, db):
        # Allow login with either email or username (OAuth2PasswordRequestForm uses the field name "username")
        user = (
            db.query(User)
            .filter(or_(User.email == username_or_email, User.username == username_or_email))
            .first()
        )
        if not user:
            return None
        if not cls.verified_password(password, user.hashed_password):
            return None
        return user

class TokenManager:

    @staticmethod
    def create_access_token(username: str, user_id: str, expires_delta: timedelta) -> str:
        expire_time = datetime.now(timezone.utc) + expires_delta

        payload = {
            "sub": username,
            "id": user_id,  
            "exp": int(expire_time.timestamp())
        }

        try:
            return jwt.encode(
                payload, 
                settings.SECRET_KEY, 
                algorithm=settings.ALGORITHM
            )
        except Exception as e:
            print(f"CRITICAL: JWT Encoding failed: {e}")
            raise e
